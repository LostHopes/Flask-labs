from flask import Blueprint

base = Blueprint(
    "base",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import views, errors