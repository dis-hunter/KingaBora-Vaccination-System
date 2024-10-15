import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'KRYTONIAN DNA'

    # Firebase configuration
    firebaseConfig = {
  "apiKey": "AIzaSyDigqFcCi42MFXvhsuaQH-0HoeWVCRIrq8",
  "authDomain": "kingaboravaccinationsystem.firebaseapp.com",
  "projectId": "kingaboravaccinationsystem",
  "storageBucket": "kingaboravaccinationsystem.appspot.com",
  "messagingSenderId": "797186497406",
  "appId": "1:797186497406:web:7ff7e514e5add24dd6f12f",
  "measurementId": "G-1WJNS5WW31",
  "databaseURL": "https://kingaboravaccinationsystem.firebaseio.com"  # Add your actual database URL here

}

    # Spotify configuration
   


     
    