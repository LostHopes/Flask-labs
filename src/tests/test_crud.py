from datetime import datetime

from app import db
from app.user.models import Users


def test_create_user(client):
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


def test_delete_user(client):
    with client.application.app_context():
        user = Users.query.filter_by(email="admin@example.com").first()
        db.session.delete(user)
        db.session.commit()
        assert user.id is not None
