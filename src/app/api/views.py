from flask import jsonify, request
import flask_jwt_extended as jwt

from datetime import timedelta

from . import api
from app.todo.models import Todo
from app.helpers.user_db import Users, UsersHelper
from app import db


@api.route("/token/generate", methods=["POST"])
def generate_token():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    helper = UsersHelper()
    succeed = helper.login(email, password)

    if not succeed:
        return jsonify({"message": "Invalid login or password"}), 401

    user = Users.query.filter_by(email=email).first()
    access_token = jwt.create_access_token(identity=user.email, expires_delta=timedelta(days=1))

    response = jsonify(token=access_token), 200

    return response


@api.route("/todos/", methods=["GET"])
@jwt.jwt_required()
def get_todos():
    identity = jwt.get_jwt_identity()
    user = Users.query.filter_by(email=identity).first()
    todos = Todo.query.filter_by(user_id=user.id).all()

    todos_list = []
    for todo in todos:
        todo_dict = {
            "id": todo.id,
            "task": todo.task,
            "status": todo.status,
            "category": todo.category
        }
        todos_list.append(todo_dict)

    response = jsonify(todos_list), 200

    return response


@api.route("/todos/", methods=["POST"])
@jwt.jwt_required()
def create_task():
    identity = jwt.get_jwt_identity()
    user = Users.query.filter_by(email=identity).first()
    data = request.get_json()
    task = data.get("task")
    todo = Todo(task=task, user_id=user.id)
    db.session.add(todo)
    db.session.commit()

    return jsonify({"message": "Task was added to the todo list"}), 201


@api.route("/todos/<int:id>")
@jwt.jwt_required()
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
@jwt.jwt_required()
def update_task(id):
    identity = jwt.get_jwt_identity()
    user = Users.query.filter_by(email=identity).first()

    todo = Todo.query.get(id)

    if not todo:
        return jsonify({"message": "Task not found"}), 404

   
    if todo.user_id != user.id:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json()
    todo.task = data.get("task")
    todo.status = data.get("status")
    todo.category = data.get("category")
    db.session.commit()

    return jsonify({"message": "Task was updated"}), 200


@api.route("/todos/<int:id>", methods=["DELETE"])
@jwt.jwt_required()
def delete_task(id):
    task = Todo.query.get(id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    identity = jwt.get_jwt_identity()
    user = Users.query.filter_by(email=identity).first()

    if task.user_id != user.id:
        return jsonify({"message": "Unauthorized"}), 401

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"The task with id {id} was deleted"}), 200
