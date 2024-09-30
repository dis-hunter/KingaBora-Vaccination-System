from flask import Blueprint, redirect, request, session, jsonify, render_template
from datetime import datetime
import requests
import urllib.parse
from config import Config
from . import spotify_bp
from flask_cors import cross_origin


CLIENT_ID = Config.CLIENT_ID
CLIENT_SECRET = Config.CLIENT_SECRET
REDIRECT_URI = Config.REDIRECT_URI
TOKEN_URL = Config.TOKEN_URL
API_BASE_URL = Config.API_BASE_URL
AUTH_URL = Config.AUTH_URL

# Blueprint definition

@spotify_bp.route('/login')
def login(): 
    scope = 'user-read-private user-read-email user-read-playback-state user-modify-playback-state'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': 'true'
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@spotify_bp.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
        
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        } 
        
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in'] 
        print(session)

        # Redirect to the frontend with a query parameter indicating auth completion
        access_token = token_info['access_token']
        return redirect(f'http://localhost:8080/?auth_completed=true&access_token={access_token}')

@spotify_bp.route('/testendpoint', methods=['GET'])
def test_endpoint():
    return jsonify({"test":"example"})
    
    
    
@spotify_bp.route('/addqueue', methods=['GET'])
def add_queue():
    track_id = request.args.get('trackId')  # Get trackId from query parameters
    if not track_id:
        return jsonify({"message": "No track ID provided"}), 400

    if 'access_token' not in session or datetime.now().timestamp() > session['expires_at']:
        return redirect('/spotify/login')

    url = 'https://api.spotify.com/v1/me/player/queue'
    access_token = session.get('access_token')
    
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    params = {
        'uri': f"spotify:track:{track_id}"
    }

    response = requests.post(url, headers=headers, params=params)
    
    if response.status_code == 204:
        result = 'Song added to queue successfully!'
        print(session)
    else:
        result = f"Error: {response.status_code} - {response.text}"

    # Redirect back to localhost with a parameter indicating completion
    return redirect('http://localhost:8080/?auth_completed=true#/')

@spotify_bp.route('/userprofile', methods=['GET'])
def get_user_profile():
    if 'access_token' not in session or datetime.now().timestamp() > session['expires_at']:
        return redirect('/spotify/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/spotify/refresh_token')

    url = 'https://api.spotify.com/v1/me'
    access_token = session.get('access_token')
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    # Retrieve user profile information
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_profile = response.json()
        username = user_profile.get('display_name', 'Unknown User')
        profile_image = user_profile['images'][0]['url'] if user_profile.get('images') else None

        # Encode the parameters
        query_params = urllib.parse.urlencode({
            'auth_completed': 'true',
            'username': username,
            'profile_image': profile_image
        })

        return jsonify({'userdetails': query_params})
    else:
        return jsonify({"error": "Failed to retrieve user profile"}), response.status_code

@spotify_bp.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/spotify/login')
        
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/spotify/refresh_token')
        
    headers={
        'Authorization': f"Bearer {session['access_token']}"
    }  
    
    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()
    
    return jsonify(playlists)     

@spotify_bp.route('/queue', methods=['GET'])
def get_queue():
    if 'access_token' not in session:
        return redirect('/spotify/login')
        
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/spotify/refresh_token')
        
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL + 'me/player/queue', headers=headers)
    queue_data = response.json()
    track_names = [track['name'] for track in queue_data['queue']]
    
    return jsonify(track_names)

@spotify_bp.route('/refresh_token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/spotify/login')  

    if datetime.now().timestamp() > session['expires_at']:
        req_body={
            'grant_type':'refresh_token',
            'refresh_token' : session['refresh_token'],
            'client_id':CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        
        return redirect('/spotify/queue')
