from flask import Blueprint

skills = Blueprint(
    "skills",
    __name__,
    static_folder="static/skills",
    template_folder="templates/skills"
)

from . import views, models
