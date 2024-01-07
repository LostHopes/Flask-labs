from datetime import datetime

from app.user.models import Users
from app import db
from tests.main import app


def test_create_user(app):
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
    assert user.id is not None