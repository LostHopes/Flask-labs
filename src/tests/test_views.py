from datetime import datetime

from tests.conftest import client


def test_home_page(client):
    """Test the root page of the site"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Home page" in response.get_data(as_text=True)


def test_about_page(client):
    """Test the about page of the site"""
    response = client.get("/about")
    assert response.status_code == 200


def test_account_page(client):
    """"""
    response = client.get("/account")
    assert response.status_code == 302


def test_users_page(client):
    """"""
    response = client.get("/users")
    assert response.status_code == 302


def test_todo_page(client):
    """"""
    response = client.get("/todo/")
    assert response.status_code == 302


def test_not_found_page(client):
    """Test page that not exists in the app"""
    response = client.get("/foo")
    assert "Page not found" in response.get_data(as_text=True)
    