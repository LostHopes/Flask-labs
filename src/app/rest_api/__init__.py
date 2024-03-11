from flask import Blueprint

rest_api = Blueprint(
    "rest_api",
    __name__
)

from .users import users_api
from .todo import todo_api
from .films import films_api