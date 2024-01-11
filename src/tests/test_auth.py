from tests.conftest import client
from app.user.models import Users


def test_register_user(client):
    response = client.post("/register", json={
        "name": "Test",
        "surname": "User",
        "login": "Test123",
        "email": "test123@gmail.com",
        "password": "password",
        "confirm_password": "password",
    })
    assert response.status_code == 200
    assert response.get_data(as_text=True)


def test_login_user(client):
    response = client.post("/login", json={
        "email": "test123@gmail.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert response.get_data(as_text=True)
    
