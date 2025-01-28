from flask import Flask, request, redirect, session, url_for, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ollama import Client
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configure Spotify API credentials from environment variables
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SCOPE = 'user-read-private user-read-email playlist-modify-public playlist-modify-private'

# Initialize Spotify OAuth
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
)

# Initialize Ollama client
ollama_client = Client(host='http://localhost:11434')

@app.route('/')
def index():
    # Redirect to Spotify login
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    # Handle the callback from Spotify
    if request.args.get("code"):
        # Get the token info
        token_info = sp_oauth.get_access_token(request.args["code"], as_dict=True)  # Add as_dict=True
        session["token_info"] = token_info
        return redirect(url_for('get_user_info'))
    return 'Error during authentication'

# @app.route('/get_user_info')
# def get_user_info():
#     # Check if user is logged in
#     if not session.get('token_info'):
#         return redirect('/')
    
#     try:  # Add error handling
#         # Create Spotify client
#         sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        
#         # Get user info
#         user_info = sp.current_user()
#         return f"Logged in as {user_info['display_name']}"
#     except Exception as e:
#         session.clear()
#         return redirect('/')
    
@app.route('/get_user_info')
def get_user_info():
    if not session.get('token_info'):
        return redirect('/')
    
    try:
        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        user_info = sp.current_user()
        return render_template('mood_form.html', username=user_info['display_name'])
    except Exception as e:
        session.clear()
        return redirect('/')

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    if not session.get('token_info'):
        return redirect('/')
    
    try:
        mood_prompt = request.form.get('mood_prompt')
        
        # Use Ollama to generate song suggestions with a more explicit prompt
        system_prompt = """You are a music expert. Based on the user's mood, suggest exactly 5 songs.
        You must respond with ONLY a JSON array of objects, each with 'artist' and 'track' keys.
        Example format:
        [
            {"artist": "The Beatles", "track": "Here Comes the Sun"},
            {"artist": "Bob Marley", "track": "Three Little Birds"}
        ]
        Do not include any other text or explanation in your response."""
        
        response = ollama_client.chat(model='mistral', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f"Suggest songs for someone who says: {mood_prompt}"}
        ])
        
        # Add debug print to see the raw response
        print("Ollama response:", response['message']['content'])
        
        try:
            # Clean the response - remove any markdown formatting if present
            content = response['message']['content']
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0]
            elif '```' in content:
                content = content.split('```')[1].split('```')[0]
            
            # Strip any whitespace and ensure we have valid JSON
            content = content.strip()
            songs = json.loads(content)
            
            # Validate the response format
            if not isinstance(songs, list):
                raise ValueError("Response is not a list")
            for song in songs:
                if not isinstance(song, dict) or 'artist' not in song or 'track' not in song:
                    raise ValueError("Invalid song format in response")
            
            # Create Spotify client
            sp = spotipy.Spotify(auth=session['token_info']['access_token'])
            user_id = sp.current_user()['id']
            
            # Create a new playlist
            playlist = sp.user_playlist_create(user_id, f"Mood Playlist: {mood_prompt[:30]}")
            
            # Search for and add songs to the playlist
            track_uris = []
            for song in songs:
                # Search for the track
                query = f"track:{song['track']} artist:{song['artist']}"
                result = sp.search(query, type='track', limit=1)
                
                if result['tracks']['items']:
                    track_uris.append(result['tracks']['items'][0]['uri'])
            
            # Add tracks to playlist
            if track_uris:
                sp.playlist_add_items(playlist['id'], track_uris)
                return f"Created playlist based on your mood! Check your Spotify account."
            else:
                return "Could not find any of the suggested songs on Spotify."
                
        except json.JSONDecodeError as e:
            return f"Error parsing AI response: {str(e)}. Raw response: {response['message']['content']}"
        except ValueError as e:
            return f"Invalid response format: {str(e)}"
            
    except Exception as e:
        return f"Error creating playlist: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
