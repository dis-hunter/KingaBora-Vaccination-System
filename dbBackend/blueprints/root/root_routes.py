from flask import Blueprint, render_template,session
from . import root_bp

@root_bp.route('/', methods=['GET'])
def login():
    # Use render_template to render the HTML file from the templates directory
    return render_template('login.html')

@root_bp.route('/signup', methods=['GET'])
def signup():
    # Use render_template to render the HTML file from the templates directory
    return render_template('Signup.html')

@root_bp.route('/dashboard', methods=['GET'])
def dashboard():
    # Use render_template to render the HTML file from the templates directory
    username = session.get('username')
    return render_template('dashboard.html')

