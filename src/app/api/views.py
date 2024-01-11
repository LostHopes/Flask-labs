from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from . import api
from app.todo.models import Todo
from app import db

# TODO: generate and refresh jwt token

@api.route("/token/generate")
def generate_token():
    pass


@api.route("/token/refresh")
def refresh_token():
    pass


@api.route("/todos/")
@jwt_required()
def get_todos():
    current_user = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=current_user).all()
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
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    data = request.get_json()
    task = data.get("task")
    user_id = current_user
    todo = Todo(task=task, user_id=user_id)
    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "Task was added to the todo list"}), 201

@api.route("/todos/<int:id>")
@jwt_required()
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
@jwt_required()
def update_task(id):
    todo = Todo.query.get(id)

    if not todo:
        return jsonify({"message": "Task not found"}), 404

    current_user = get_jwt_identity()

    if todo.user_id != current_user:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    todo.task = data.get("task")
    todo.status = data.get("status")
    todo.category = data.get("category")
    db.session.commit()

    return jsonify({"message": "Task was updated"}), 200

@api.route("/todos/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    task = Todo.query.get(id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    current_user = get_jwt_identity()

    if task.user_id != current_user:
        return jsonify({"message": "Unauthorized"}), 401

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"The task with id {id} was deleted"}), 200
