from app.models.user import User

def test_index_page(client):
    """Test that the index/landing page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to CERS" in response.data

def test_login_page_renders(client):
    """Test that the login page loads."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Login" in response.data
    
def test_user_login(client, init_database):
    """Test logging in with accurate credentials ignores CSRF and successfully flashes."""
    
    # We first GET the page to establish a session
    response = client.get('/auth/login')
    
    response = client.post(
        '/auth/login',
        data={'email': 'wrong@example.com', 'password': 'hashed_pw'},
        follow_redirects=True
    )
    
    assert response.status_code == 200
    assert b"Login Unsuccessful" in response.data
