from flask import Blueprint

root_bp = Blueprint('root_bp', __name__, template_folder='../../templates')

# Import routes at the end to avoid circular import
from . import root_routes
