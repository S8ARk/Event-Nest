import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("CRITICAL: No SECRET_KEY set for Flask application. You must define this in your .env configuration.")
        
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'cers.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # NLP Engine Constants
    MIN_SCORE_THRESHOLD = float(os.environ.get('MIN_SCORE_THRESHOLD', 15.0))

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # In-memory DB for tests
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret' # Safe fallback solely for CI/CD test frameworks
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # In-memory DB for tests
    WTF_CSRF_ENABLED = False
