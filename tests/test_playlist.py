import unittest
from unittest.mock import patch
from app import create_app
from config.settings import TestConfig

class PlaylistTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    @patch('app.services.spotify.get_spotify_client')
    def test_mood_form_requires_auth(self, mock_spotify):
        response = self.client.get('/mood')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    @patch('app.services.ollama.generate_song_suggestions')
    def test_create_playlist_requires_auth(self, mock_ollama):
        response = self.client.post('/create_playlist')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)