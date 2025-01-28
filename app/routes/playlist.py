from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.spotify import get_spotify_client
from app.services.ollama import generate_song_suggestions

playlist_bp = Blueprint('playlist', __name__)

@playlist_bp.route('/mood', methods=['GET'])
def mood_form():
    """Display mood input form"""
    if not session.get('token_info'):
        return redirect(url_for('auth.login'))
    
    try:
        sp = get_spotify_client()
        user_info = sp.current_user()
        return render_template('mood_form.html', username=user_info['display_name'])
    except Exception as e:
        flash('Error accessing Spotify. Please try logging in again.', 'error')
        return redirect(url_for('auth.logout'))

@playlist_bp.route('/create_playlist', methods=['POST'])
def create_playlist():
    """Create playlist based on mood"""
    if not session.get('token_info'):
        return redirect(url_for('auth.login'))
    
    try:
        mood_prompt = request.form.get('mood_prompt')
        if not mood_prompt:
            flash('Please enter your mood', 'error')
            return redirect(url_for('playlist.mood_form'))

        # Get song suggestions from AI
        songs = generate_song_suggestions(mood_prompt)
        
        # Create playlist
        sp = get_spotify_client()
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(
            user_id, 
            f"Mood Playlist: {mood_prompt[:30]}", 
            description=f"Generated based on mood: {mood_prompt}"
        )
        
        # Search and add songs
        track_uris = []
        for song in songs:
            query = f"track:{song['track']} artist:{song['artist']}"
            result = sp.search(query, type='track', limit=1)
            if result['tracks']['items']:
                track_uris.append(result['tracks']['items'][0]['uri'])
        
        if track_uris:
            sp.playlist_add_items(playlist['id'], track_uris)
            flash('Playlist created successfully!', 'success')
        else:
            flash('No matching songs found on Spotify.', 'warning')
            
        return redirect(url_for('playlist.mood_form'))
        
    except Exception as e:
        flash(f'Error creating playlist: {str(e)}', 'error')
        return redirect(url_for('playlist.mood_form'))