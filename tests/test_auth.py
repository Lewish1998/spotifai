import unittest
from app import create_app
from config.settings import TestConfig

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_index_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_login_redirect(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 302)