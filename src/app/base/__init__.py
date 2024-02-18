from flask import Blueprint

base = Blueprint(
    "base",
    __name__,
    static_folder="static/base",
    template_folder="templates/base"
)

from . import views, errors