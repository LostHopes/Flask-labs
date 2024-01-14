from flask import Blueprint

films = Blueprint(
    "films",
    __name__,
    template_folder="templates",
    static_folder="static"
)

from . import views