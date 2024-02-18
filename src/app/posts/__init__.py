from flask import Blueprint

posts = Blueprint(
    "posts",
    __name__,
    static_folder="static/posts",
    template_folder="templates/posts"
)

from . import forms, models, views