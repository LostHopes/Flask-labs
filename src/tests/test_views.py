from datetime import datetime

from tests.conftest import client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200


