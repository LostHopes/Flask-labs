from flask import Blueprint

user = Blueprint(
    "user",
    __name__,
    static_folder="static/user",
    template_folder="templates/user"
)

from . import views, forms, models