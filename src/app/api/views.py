from flask import jsonify

from . import api
from app.todo.models import Todo
from app import db


@api.route("/todos")
def get_todos():
    todos = Todo.query.all()
    todos_json = []
    for todo in todos:
        todo_dict = {
            "id": todo.id,
            "task": todo.task,
            "status": todo.status,
            "category": todo.category,
            "user_id": todo.user_id
        }
        todos_json.append(todo_dict)
    return jsonify(todos_json)


@api.route("/todos", methods=["POST"])
def create_task():
    pass

@api.route("/todos/<int:id>")
def get_task(id):
    task = Todo.query.get(id)
    # TODO: handle errors
    return jsonify({
        "id": task.id,
        "task": task.task,
        "status": task.status,
        "category": task.category,
        "user_id": task.user_id
    })

@api.route("/todos/<int:id>", methods=["PUT"])
def update_task(id):
    pass

@api.route("/todos/<int:id>", methods=["DELETE"])
def delete_task(id):
    # TODO: handle errors
    task = Todo.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"The task with id {id} was deleted"})


