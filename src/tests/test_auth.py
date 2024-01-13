from datetime import datetime
from flask_login import login_user

from tests.conftest import client
from app.user.models import Users


def test_register_user(client):
    """Test register user using register form"""
    data = {
        "name": "Test123",
        "surname": "User123",
        "login": "Test123456",
        "email": "test123456@gmail.com",
        "password": "password123",
        "confirm_password": "password123",
    }
    response = client.get("/register", data=data, follow_redirects=True)
    assert response.status_code == 200


def test_login_user(client):
    """Test register user using login form"""
    
    data = {
        "email": "test@example.com",
        "password": "password"
    }
    user = Users.query.filter_by(email="test@gmail.com").first()
    login_user(user, remember=True)
    response = client.get("/login", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/account"
    assert b"Account info" in response.data
    assert len(response.history) == 1


def test_update_account(client):
    response = client.get("/account", follow_redirects=True)
    user = Users.query.filter_by(email="test@gmail.com").first()
    user.about = "Test about me!"
    assert response.status_code == 200
    assert response.request.path == "/account"
    assert b"Test about me!" in response.data


def test_logout_user(client):
    """Test logout user"""
    response = client.post("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
    assert len(response.history) == 1
    assert B"You have successfully logged out" in response.data

