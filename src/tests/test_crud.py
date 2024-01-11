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



def test_delete_user(client):
    """Test deleting a user"""
    with client.application.app_context():
        user = Users.query.filter_by(email="admin@example.com").first()
        db.session.delete(user)
        db.session.commit()
        assert user.id is not None
