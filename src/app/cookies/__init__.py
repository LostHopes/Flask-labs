from flask import Blueprint

cookies = Blueprint(
    "cookies",
    __name__,
    static_folder="static",
    template_folder="templates/cookies"
)

from . import views, forms