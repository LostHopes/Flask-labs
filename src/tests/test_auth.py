from tests.conftest import client
from app.user.models import Users


def test_register_user(client):
    """Test register user using register form"""
    response = client.post("/register", json={
        "name": "Test",
        "surname": "User",
        "login": "Test123",
        "email": "test123@gmail.com",
        "password": "password",
        "confirm_password": "password",
    })
    assert response.status_code == 200


def test_login_user(client):
    """Test register user using login form"""
    response = client.post("/login", json={
        "email": "test123@gmail.com",
        "password": "password"
    })
    assert response.status_code == 200
