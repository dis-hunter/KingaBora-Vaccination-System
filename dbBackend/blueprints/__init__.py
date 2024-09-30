from flask import Flask
from blueprints.spotify import spotify_bp
from blueprints.firebase import firebase_bp
from blueprints.root import root_bp

from config import Config

def create_app():
    app = Flask(__name__, template_folder='../templates')

    # Load the configuration
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(spotify_bp, url_prefix='/spotify')
    app.register_blueprint(firebase_bp, url_prefix='/firebase')
    app.register_blueprint(root_bp, url_prefix='/')

    return app
