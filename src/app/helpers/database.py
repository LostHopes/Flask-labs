from flask_sqlalchemy import SQLAlchemy
from app.models import db, Todo, Users
from app import app


with app.app_context():
    db.create_all(bind_key=None)

class HandleUsers(Users):
    def remove(self):
        pass

    def add(self):
        pass


class HandleTodos(Todo):
    def show(self):
        query = db.session.query(Todo)
        return query

    def remove(self):
        pass

    def add(self, name: str):
        task = Todo(task=name)
        db.session.add(task)
        db.session.commit()
        return name
