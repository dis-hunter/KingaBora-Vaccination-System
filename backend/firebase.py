from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_cors import CORS

import pyrebase
from flask_caching import Cache
import firebase_admin
from firebase_admin import credentials, firestore, auth, initialize_app
from config import Config
from datetime import datetime, timedelta
import os
import requests

firebase_config = Config.firebaseConfig

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Construct the absolute path to the service account key file
base_dir = os.path.dirname(os.path.abspath(__file__))
service_key_path = os.path.normpath(os.path.join(base_dir, 'kingaboravaccinationsystem-firebase-adminsdk-4vd5w-29da0d42b8.json'))
# Initialize Firebase Admin SDK

cred = credentials.Certificate(service_key_path)
firebase_admin.initialize_app(cred, {'projectId': 'kingaboravaccinationsystem'})
db = firestore.client()
# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# Set a secret key if using sessions or forms
app.secret_key = 'your_secret_key'

# create a user using firebase authenticate
@app.route('/register', methods=['POST'])  # Change to POST for better practice
def register():
    data = request.get_json()  # Get JSON data from the request

    # Extract data from the request
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "Missing email, username, or password"}), 400

    # Your logic to create user in Firebase (replace with your implementation)
    # Assuming successful creation...
    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user_with_email_and_password(email, password)
        local_id = user['localId']

        # Here you might want to store the username and other user details in your database
        redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/landingpage/altIndex.html"

        return jsonify({"message": "Successfully created the user", "localId": local_id, "redirectUrl": redirect_url}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return error message
    
# Example route to handle POST requests
@app.route('/email_authenticate', methods=['POST'])
def email_authenticate():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Sign in the user with Firebase
        user = auth.sign_in_with_email_and_password(email, password)
        local_id = user['localId']

        # Example: Fetch user data from Firestore (optional, you can expand based on your use case)
        # user_data = firestore_db.collection('users').document(local_id).get()
        # username = user_data.to_dict().get('username', 'User')

        # Store user information in session (optional)
        session['local_id'] = local_id
        # session['username'] = username

        # Return JSON response with redirect URL
        redirect_url = "http://localhost:8080/KingaBora-Vaccination-System/landingpage/altIndex.html"
        return jsonify({"message": "Successfully logged in", "localId": local_id, "redirectUrl": redirect_url}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/childDetails', methods=['GET'])

def ChildDetails():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Extract the BirthCertificateID from the form data
        birth_certificate_id = data.get("BirthCertificateID")
        
        if not birth_certificate_id:
            return jsonify({"error": "BirthCertificateID is required"}), 400

        # Reference to the 'childData' collection
        child_data_ref = db.collection('childData')
        
        # Query Firestore to find the document with the matching BirthCertificateID
        query = child_data_ref.where('BirthCertificate ID', '==', birth_certificate_id).stream()

        # Initialize result to None
        child_doc = None
        
        # Process the query results
        for doc in query:
            child_doc = doc.to_dict()  # Get the document data if found
            child_doc["doc_id"] = doc.id  # Optionally include document ID

        if child_doc:
            return jsonify({"message": "Child found", "childData": child_doc}), 200
        else:
            return jsonify({"error": "No child found with the given BirthCertificateID"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message on exception

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Running on localhost:5000
