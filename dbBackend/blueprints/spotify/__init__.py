from flask import Blueprint

spotify_bp = Blueprint('spotify', __name__)

from . import spotify_routes
