from tests.conftest import client, db
from app.user.models import Users


def test_register_user(client):
    """Test register user using register form"""
    data = dict(
        name = "Test",
        surname="User",
        login="Test12345",
        email="test12345@gmail.com",
        password="password",
        confirm_password="password",
    )
    response = client.post("/register", data=data, follow_redirects=True)
    assert response.status_code == 200


def test_login_user(client):
    """Test register user using login form"""
    data = dict(
        email="test12345@gmail.com",
        password="password123"
    )
    with client.application.app_context():
        user = Users.query.filter_by(email="test12345@gmail.com").first()
        client.delete(f"/api/users/{user.id}")
        response = client.post("/login", data=data, follow_redirects=True)
        assert response.status_code == 200
