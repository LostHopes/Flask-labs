from flask import Blueprint

cookies = Blueprint(
    "cookies",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import views, forms