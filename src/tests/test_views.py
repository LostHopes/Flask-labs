from datetime import datetime

from tests.conftest import client
from app import db
from app.user.models import Users


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200


