from flask import Blueprint

todo = Blueprint(
    "todo",
    __name__,
    static_folder="static/todo",
    template_folder="templates/todo"
)

from . import views, forms, models