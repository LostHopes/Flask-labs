from flask import Blueprint

posts = Blueprint(
    "posts",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import forms, models, views