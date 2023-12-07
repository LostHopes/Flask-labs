from flask import jsonify

from . import api
from app.todo.models import Todo


@api.route("/todos")
def get_todos():
    pass

@api.route("/todos", methods=["POST"])
def create_task():
    pass

@api.route("/todos/<int:id>")
def get_task(id):
    pass

@api.route("/todos/<int:id>", methods=["PUT"])
def update_task(id):
    pass

@api.route("/todos/<int:id>", methods=["DELETE"])
def delete_task(id):
    pass


