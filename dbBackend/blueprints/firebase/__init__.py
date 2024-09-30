from flask import Blueprint

firebase_bp=Blueprint('firebase', __name__,template_folder='../../templates')
from . import firebase_routes