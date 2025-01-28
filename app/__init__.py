from flask import Flask
from config.settings import Config
from flask_session import Session
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config_class)
    
    # Ensure secret key is set
    if not app.secret_key:
        app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-please-change')
    
    # Initialize Flask-Session
    Session(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.playlist import playlist_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(playlist_bp)
    
    # Register error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    return app