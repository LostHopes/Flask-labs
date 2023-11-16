from flask_sqlalchemy import SQLAlchemy
from app.models import db, Todo, Users
from app import app


with app.app_context():
    db.create_all()
    print("Database created")


class HandleUsers(Users):
    def __init__(self):
        pass

    def remove(self):
        pass

    def add(self):
        pass


class HandleTodos(Todo):
    def __init__(self):
        pass

    def remove(self):
        pass

    def add(self):
        pass