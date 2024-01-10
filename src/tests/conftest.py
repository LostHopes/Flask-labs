import pytest
from app import create_app, db


@pytest.fixture(scope="session", autouse=True)
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client



