from flask import Blueprint, redirect, session, url_for, request, render_template
from app.services.spotify import get_spotify_oauth, get_spotify_client

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Landing page route"""
    if session.get('token_info'):
        return redirect(url_for('playlist.mood_form'))
    return render_template('index.html')

@auth_bp.route('/login')
def login():
    """Initiate Spotify OAuth flow"""
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@auth_bp.route('/callback')
def callback():
    """Handle Spotify OAuth callback"""
    sp_oauth = get_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('playlist.mood_form'))

@auth_bp.route('/logout')
def logout():
    """Clear session and logout"""
    session.clear()
    return redirect(url_for('auth.index'))