from app import db
from app.todo.models import Todo


class TodosHelper(Todo):
    def show(self, id):
        todos = db.session.query(Todo).where(Todo.user_id == id)
        return todos

    def remove(self, id: int | None):
        todo = Todo.query.filter_by(id=id).first()
        db.session.delete(todo)
        db.session.commit()

    def add(self, name: str, id: int):
        task = Todo(task=name, user_id=id)
        db.session.add(task)
        db.session.commit()

    def update(self, id: int):
        task = db.session.query(Todo).filter(Todo.id == id).first()
        task.status = "Completed"
        db.session.commit()
