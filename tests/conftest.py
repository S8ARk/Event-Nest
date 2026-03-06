import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app('app.config.TestingConfig')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Create a test user
        from app import bcrypt
        pw = bcrypt.generate_password_hash('hashed_pw').decode('utf-8')
        user = User(name='Test User', email='test@example.com', password_hash=pw, role='student')
        db.session.add(user)
        db.session.commit()
        yield db
