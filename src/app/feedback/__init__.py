from flask import Blueprint

feedback = Blueprint(
    "feedback",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import forms, models, views