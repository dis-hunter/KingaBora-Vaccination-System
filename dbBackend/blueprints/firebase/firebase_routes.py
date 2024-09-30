from . import firebase_bp
from flask import Flask, request, jsonify, session, redirect, url_for, render_template
import pyrebase
from flask_caching import Cache
import firebase_admin
from firebase_admin import credentials, firestore, auth, initialize_app
from config import Config
from datetime import datetime, timedelta
import os
import requests

# Retrieve firebaseConfig from Config
firebase_config = Config.firebaseConfig
google_config = Config.web

# Initialize Firebase using pyrebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Construct the absolute path to the service account key file
base_dir = os.path.dirname(os.path.abspath(__file__))
service_key_path = os.path.normpath(os.path.join(base_dir, '../../../servicekey/jukebox-996de-firebase-adminsdk-9n2km-3f149867fb.json'))

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_key_path)
firebase_admin.initialize_app(cred, {'projectId': 'jukebox-996de'})
db = firestore.client()

@firebase_bp.route('/', methods=['GET'])
def root():
    # Use send_from_directory to render the HTML file from the root directory
    return render_template('login.html')

@firebase_bp.route('/register', methods=['POST'])
def register():
    # try:
        # Get form data
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # Create a new user in Firebase Authentication
        user = auth.create_user_with_email_and_password(email, password)
        local_id = user['localId']
        
        

        # Data to be added to Firestore
        user_data = {
            'username': username,
            'email': email,
            
            # Add more fields as needed
        }
        
        # Add data to Firestore
        db.collection('users').document(local_id).set(user_data)
        session['user_id'] = local_id
        session['username'] = username


        # Optionally, set session variables or perform other post-registration logic

        # Redirect to login page after successful registration
        return redirect('/dashboard')
    # except Exception as e:
    #     return render_template('error.html', message=str(e))


@firebase_bp.route('/email_authenticate', methods=['POST'])
def email_authenticate():
    try:
        # Get form data
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Sign in the user
        user = auth.sign_in_with_email_and_password(email, password)
        local_id = user['localId']

        # Retrieve user data from Firestore
        user_doc = db.collection('users').document(local_id).get()
        username = user_doc.get('username')  # Assuming 'username' is a field in your Firestore document
        print("welcome")
        
        # Store the local_id and username in the session
        session['local_id'] = local_id
        session['username'] = username
        session.modified = True
        print(session)

        # Return a JSON response with the local_id, username, message, and redirect URL
        return jsonify({
            "message": "Authentication successful.",
            "local_id": local_id,
            "username": username,
            "redirect_url": "http://127.0.0.1:5000/spotify/login"
        })

    except Exception as e:
        # In case of error, return the error message
        return jsonify({"error": str(e)}), 500



    
@firebase_bp.route('/google_authenticate', methods=['GET'])
def google_authenticate():
    # Generate the Google OAuth2 URL
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={google_config['client_id']}&"
        f"redirect_uri={google_config['redirect_uris']}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile"
    )
    
    return jsonify({"auth_url": google_auth_url})


@firebase_bp.route('/callback', methods=['GET'])
def callback():
    auth_code = request.args.get('code')

    if not auth_code:
        return "Authorization code not provided.", 400

    token_data = {
        'code': auth_code,
        'client_id': google_config['client_id'],
        'client_secret': google_config['client_secret'],
        'redirect_uri': google_config['redirect_uris'],
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(google_config['token_uri'], data=token_data)
    token_response_data = token_response.json()

    if 'error' in token_response_data:
        return f"Error retrieving access token: {token_response_data['error_description']}", 400

    id_token = token_response_data.get('id_token')

    if not id_token:
        return "ID token not retrieved.", 400

    try:
        decoded_token = firebase_admin.auth.verify_id_token(id_token)
        local_id = decoded_token['uid']
        username = decoded_token.get('name', 'Unknown User')

        session['user'] = decoded_token

        return jsonify({
            "message": "Authentication successful.",
            "local_id": local_id,
            "username": username,
            "redirect_url": "http://127.0.0.1:5000/spotify/login"
        })
    except Exception as e:
        return f"Error verifying ID token: {str(e)}", 400


    


@firebase_bp.route('/redirectagain', methods=['POST'])
def redirectagain():
    return redirect('/uploadtrack')
@firebase_bp.route('/uploadtrack', methods=['POST'])
def upload():
    try:
        # Assuming sender_id is retrieved from session or some other authentication mechanism
        sender_id = request.headers.get('Authorization').replace('Bearer ', '')
        
        # Parse JSON data from request
        data = request.get_json()
        track_id = data.get('track')
        note = data.get('note')
        selected_friends = data.get('friends', [])  # List of selected friend IDs

        # Iterate over each selected friend and create a record in Firestore
        for friend_id in selected_friends:
            user_data = {
                'sender': sender_id,
                'receiver': friend_id,
                'note': note,
                'viewed': False,
                'trackid': track_id,  # Sample track ID, update as needed
                'timestamp': firestore.SERVER_TIMESTAMP  # Add the current server timestamp
            }
            db.collection('messages').add(user_data)

        return jsonify({"message": "Track uploaded successfully to all selected friends."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500






@firebase_bp.route('/receivedtrack', methods=['GET'])
def receivedtrack():
    try:
        local_id = request.headers.get('Authorization').replace('Bearer ', '')

        # Simplified query without ordering
        track_ref = db.collection('messages') \
            .where('receiver', '==', local_id) \
            .where('viewed', '==', False)
        
        docs = track_ref.stream()

        tracks = []
        for doc in docs:
            track_data = doc.to_dict()
            track_id = track_data.get('trackid')
            friend_id = track_data.get('sender')
            timestamp = track_data.get('timestamp')

            if not timestamp:
                continue

            if track_id and friend_id:
                friend_doc = db.collection('users').document(friend_id).get()
                if friend_doc.exists:
                    friend_username = friend_doc.to_dict().get('username')
                    tracks.append({
                        'track_id': track_id,
                        'friend_username': friend_username,
                        'timestamp': timestamp
                    })

        # Sort in memory
        tracks.sort(key=lambda x: x['timestamp'], reverse=True)

        return jsonify({'tracks': tracks})

    except Exception as e:
        print(f"Error in receivedtrack: {str(e)}")
        return jsonify({"error": str(e)}), 500



@firebase_bp.route('/getFriends', methods=['GET'])
def get_friends():
    try:
        user_id = request.headers.get('Authorization').replace('Bearer ', '')
        # Reference to the 'friends' subcollection
        friends_ref = db.collection('users').document(user_id).collection('Friends')
        docs = friends_ref.stream()

        friends_list = []
        for doc in docs:
            friend_data = doc.to_dict()
            friends_list.append({
                'localid': doc.id,
                'userid': friend_data.get('userid'),
                'username': friend_data.get('username')
            })

        return jsonify({'friends': friends_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




 


if __name__ == '__main__':
    app.run(debug=True)
