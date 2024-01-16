# Лабораторна №12 Тестування

# 1. Тестування з допомогою фреймворка pytest з плагіном coverage

Конфігурація тестів у файлі *conftest.py*

```python
import pytest

from app import create_app, db
from app.user.models import Users


@pytest.fixture(scope="session", autouse=True)
def app():
    """Create app for testing"""
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    ctx = app.test_request_context()
    ctx.push()
    yield app
    with app.app_context():
        db.session.remove()
    
    ctx.pop()


@pytest.fixture
def client(app):
    """Create test client 
    to pass as an argument to other tests"""
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def runner(app):
    yield app.test_cli_runner()
    
```

## 1.1 Маршрути (routes)

```python
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
    response = client.get("/todo/list")
    assert response.status_code == 302


def test_not_found_page(client):
    """Test page that not exists in the app"""
    response = client.get("/foo")
    assert response.status_code == 404
    assert "Not Found" in response.get_data(as_text=True)

```

## 1.2 CRUD

Вміст файла *test_crud.py*

```python
from datetime import datetime

from app import db
from app.user.models import Users


def test_create_user(client):
    """Test creating a user"""
    with client.application.app_context():
        user = Users(
            login="admin",
            email="admin@example.com",
            password="password",
            name="Admin",
            surname="Admin",
            register_date=datetime.now().replace(second=0, microsecond=0)
        )
        db.session.add(user)
        db.session.commit()
        assert user.is_authenticated
        assert user.is_active
        assert not user.is_anonymous


def test_user_info(client):
    """Test user info"""
    with client.application.app_context():
        email = "admin@example.com"
        user = Users.query.filter_by(email=email).first()
        assert user.email == email


def test_user_update(client):
    """Test updating the user"""
    with client.application.app_context():
        user = Users.query.filter_by(login="admin").first()
        user.login = "user"
        user.email = "user@example.com"
        db.session.commit()


def test_delete_user(client):
    """Test deleting a user"""
    with client.application.app_context():
        user = Users.query.filter_by(email="user@example.com").first()
        db.session.delete(user)
        db.session.commit()
        assert user.id is not None

```

## 1.3 Авторизація

```python
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


```

# 2. Виконання тестів у режимі verbose

![image](/screenshots/lab12/lab12_1.png)

# 3. Виконання pytest з розширенням coverage

![image](/screenshots/lab12/lab12_2.png)

# 4. Звіт покриття у форматі html

```
python -v --cov --cov-report html
```