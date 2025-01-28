from ollama import Client
import json

client = Client(host='http://localhost:11434')

def generate_song_suggestions(mood_prompt):
    """Generate song suggestions based on mood using Ollama"""
    system_prompt = """You are a music expert. Based on the user's mood, suggest 5 songs.
    You must respond with ONLY a JSON array of objects, each with 'artist' and 'track' keys.
    Example format:
    [
        {"artist": "The Beatles", "track": "Here Comes the Sun"},
        {"artist": "Bob Marley", "track": "Three Little Birds"}
    ]
    Do not include any other text in your response."""
    
    try:
        response = client.chat(model='mistral', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f"Suggest songs for someone who says: {mood_prompt}"}
        ])
        
        content = response['message']['content']
        
        # Clean the response
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        
        songs = json.loads(content.strip())
        
        # Validate response format
        if not isinstance(songs, list):
            raise ValueError("Invalid response format: not a list")
        
        for song in songs:
            if not isinstance(song, dict) or 'artist' not in song or 'track' not in song:
                raise ValueError("Invalid song format in response")
        
        return songs
        
    except Exception as e:
        raise Exception(f"Error generating song suggestions: {str(e)}")