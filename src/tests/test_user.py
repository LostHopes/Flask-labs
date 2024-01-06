from datetime import datetime

from tests.base import BaseTest, db
from app.user.models import Users

class TestUser(BaseTest):
    def test_create_user(self):
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