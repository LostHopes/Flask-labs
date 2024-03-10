from tests.conftest import client
from app.user.models import Users


def test_create_user(client):
    json = {
        "login": "test123",
        "email": "test123@gmail.com",
        "password": "password123",
        "confirm_password": "password123",
        "name": "Test123",
        "surname": "Test123",
        "register_date": "2024-02-13 16:54:00"
    }
    response = client.post("/api/users", json=json)
    assert response.status_code == 200


def test_list_users(client):
    response = client.get("/api/users")
    assert "test123@gmail.com" in response.get_data(as_text=True)
    assert response.status_code == 200


def test_update_user(client):
    with client.application.app_context():
        user = Users.query.filter_by(email="test123@gmail.com").first()
        json = {
            "login": "test1234",
            "email": "test1234@gmail.com",
            "password": "password1234",
            "confirm_password": "password1234",
            "last_seen": "2024-02-13 16:55:00",
            "about": "test1234"
        }

        response = client.put(f"/api/users/{user.id}", json=json)
        assert response.status_code == 200


def test_delete_user(client):
    with client.application.app_context():
        user = Users.query.filter_by(email="test1234@gmail.com").first()
        response = client.delete(f"/api/users/{user.id}")
        assert response.status_code == 200


def test_list_todo(client):
    pass


def test_create_task(client):
    pass


def test_update_task(client):
    pass


def test_delete_task(client):
    pass


def test_list_films(client):
    pass


def test_add_film(client):
    pass


def test_update_film(client):
    pass


def test_delete_film(client):
    pass



