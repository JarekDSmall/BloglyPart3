import pytest
from app import app, db
from models import User

# Enable app testing mode and use an in-memory SQLite database
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_ECHO'] = False

# Define a test client for making requests
client = app.test_client()

@pytest.fixture
def new_user():
    return User(username='testuser')

def test_index_redirect():
    response = client.get('/')
    assert response.status_code == 302  # Redirect status code

def test_show_users_empty():
    response = client.get('/users')
    assert b'No users found.' in response.data

def test_add_user():
    response = client.post('/users/new', data={'username': 'newuser'}, follow_redirects=True)
    assert b'newuser' in response.data

def test_user_detail(new_user):
    db.session.add(new_user)
    db.session.commit()
    response = client.get(f'/users/{new_user.id}')
    assert new_user.username.encode() in response.data

def test_edit_user(new_user):
    db.session.add(new_user)
    db.session.commit()
    response = client.post(f'/users/{new_user.id}/edit', data={'username': 'updateduser'}, follow_redirects=True)
    assert b'updateduser' in response.data

def test_delete_user(new_user):
    db.session.add(new_user)
    db.session.commit()
    response = client.post(f'/users/{new_user.id}/delete', follow_redirects=True)
    assert b'No users found.' in response.data
