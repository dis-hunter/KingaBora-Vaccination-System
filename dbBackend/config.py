import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'KRYTONIAN DNA'

    # Firebase configuration
    firebaseConfig = {
        "apiKey": "AIzaSyAZVqG2fV1wII9BC1hFA6_qlNhuXqry3ZU",
        "authDomain": "jukebox-996de.firebaseapp.com",
        "projectId": "jukebox-996de",
        "databaseURL":"https://jukebox-996de-default-rtdb.firebaseio.com",
        "storageBucket": "jukebox-996de.appspot.com",
        "messagingSenderId": "941925661587",
        "appId": "1:941925661587:web:e8468dd133d0c5997ac666",
        "measurementId": "G-SDXVEHEQ0F"
                      }

    # Spotify configuration
    CLIENT_ID = 'a9736e527970462a878ac1113b95d52f'
    CLIENT_SECRET = '41055803e9c947ee80f9dea38820cb50'
    REDIRECT_URI = 'http://127.0.0.1:5000/spotify/callback'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    API_BASE_URL = 'https://api.spotify.com/v1/'
    AUTH_URL = 'https://accounts.spotify.com/authorize'


     
    web={
        "client_id":"141359446177-luhn1chi7kmii8qvmu91miajq8u40ua3.apps.googleusercontent.com","project_id":"kadmus-3579e",
         "auth_uri":"https://accounts.google.com/o/oauth2/auth",
         "token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":"http://127.0.0.1:5000/firebase/callback"}