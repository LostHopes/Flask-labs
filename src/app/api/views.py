from flask import jsonify, request

from . import api
from app.todo.models import Todo
from app import db


@api.route("/todos/")
def get_todos():
    todos = Todo.query.all()
    todos_list = []
    for todo in todos:
        todo_dict = {
            "id": todo.id,
            "task": todo.task,
            "status": todo.status,
            "category": todo.category,
            "user_id": todo.user_id
        }
        todos_list.append(todo_dict)
    return jsonify(todos_list), 200


@api.route("/todos/", methods=["POST"])
def create_task():
    data = request.get_json()
    task = data.get("task")
    user_id = data.get("user_id")
    todo = Todo(task=task, user_id=user_id)
    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "Task was added to the todo list"}), 201

@api.route("/todos/<int:id>")
def get_task(id):
    task = Todo.query.get(id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    return jsonify({
        "id": task.id,
        "task": task.task,
        "status": task.status,
        "category": task.category,
        "user_id": task.user_id
    }), 200

@api.route("/todos/<int:id>", methods=["PUT"])
def update_task(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json()
    todo.task = data.get("task")
    todo.status = data.get("status")
    todo.category = data.get("category")
    todo.user_id = data.get("user_id")
    db.session.commit()

    return jsonify({"message": "Task was updated"}), 200

@api.route("/todos/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Todo.query.get(id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"The task with id {id} was deleted"}), 200


