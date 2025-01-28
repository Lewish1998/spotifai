from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from flask import session, current_app
from config.settings import Config

def get_spotify_oauth():
    """Create SpotifyOAuth instance"""
    return SpotifyOAuth(
        client_id=Config.SPOTIFY_CLIENT_ID,
        client_secret=Config.SPOTIFY_CLIENT_SECRET,
        redirect_uri=Config.SPOTIFY_REDIRECT_URI,
        scope=Config.SPOTIFY_SCOPE,
        cache_handler=None  # Disable cache to prevent file system writes
    )

def get_spotify_client():
    """Get authenticated Spotify client"""
    token_info = session.get('token_info')
    if not token_info:
        raise Exception("No token info found in session")
    return Spotify(auth=token_info['access_token'])

def refresh_token_if_expired():
    """Check and refresh token if expired"""
    token_info = session.get('token_info')
    if not token_info:
        return False
        
    sp_oauth = get_spotify_oauth()
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    return True