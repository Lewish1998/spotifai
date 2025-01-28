# 🎵 Mood-Based Spotify Playlist Generator

> Transform your emotions into personalized Spotify playlists using AI!

*This project was developed with assistance from Claude AI (Anthropic)*

## 🌟 Overview

This Flask application combines the power of Spotify's API and Ollama's local AI to create custom playlists based on your mood. Simply describe how you're feeling, and watch as AI curates a playlist that matches your emotional state!

## 🚀 Features

- 🔐 Secure Spotify Authentication
- 🤖 AI-powered song selection
- 🎵 Automatic playlist creation
- 📝 Mood-based playlist naming
- 🏃‍♂️ Runs completely locally

## 📋 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) installed locally
- Spotify account
- Spotify Developer account

## 🛠️ Installation & Setup

### 1. Clone & Install
```bash
Clone the repository
git clone <your-repository-url>
cd <repository-name>
Create and activate virtual environment
python -m venv venv
Windows
venv\Scripts\activate
macOS/Linux
source venv/bin/activate
Install dependencies
pip install flask spotipy python-dotenv ollama
```


### 2. Spotify Configuration

1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Add `http://localhost:5000/callback` to your Redirect URIs in app settings
4. Save your Client ID and Client Secret

### 3. Ollama Setup
```bash
Install Ollama from ollama.ai
Then pull the Mistral model
ollama pull mistral
```

### 4. Environment Setup

Create a `.env` file in the project root:

```env
FLASK_SECRET_KEY=your-secure-secret-key
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
```

## 🎮 Usage

1. Start Ollama in the background
2. Run the Flask app:
   ```bash
   python main.py
   ```
3. Navigate to `http://localhost:5000`
4. Log in with Spotify
5. Enter your mood
6. Enjoy your AI-curated playlist!

## 📁 Project Structure
mood-playlist-generator/
├── main.py # Flask application
├── templates/ # HTML templates
│ └── mood_form.html # Mood input form
├── .env # Environment variables
├── .gitignore # Git ignore file
└── README.md # Documentation


## ⚠️ Common Issues & Solutions

### Spotify Authentication Issues
- Clear browser cookies
- Delete `.cache` file
- Restart application

### Ollama Errors
- Verify Ollama is running (`ps aux | grep ollama`)
- Check Mistral model installation (`ollama list`)
- Ensure port 11434 is available

### Playlist Creation Fails
- Verify Spotify credentials
- Check internet connection
- Confirm API scopes are correct

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- Built with assistance from [Claude AI](https://anthropic.com/claude)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [Ollama](https://ollama.ai)
- [Flask](https://flask.palletsprojects.com/)
- [Spotipy](https://spotipy.readthedocs.io/)

## 📫 Support

Having issues? Let us know:
1. Check existing issues or create a new one
2. Provide detailed information about your problem
3. Include error messages and screenshots if possible

---

<p align="center">
  Made with ❤️ and AI
</p>