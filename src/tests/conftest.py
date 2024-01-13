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
    



