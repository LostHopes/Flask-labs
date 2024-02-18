from flask import Blueprint

feedback = Blueprint(
    "feedback",
    __name__,
    static_folder="static/feedback",
    template_folder="templates/feedback"
)

from . import forms, models, views