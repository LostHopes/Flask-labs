from flask import Blueprint

skills = Blueprint(
    "skills",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import views, models
