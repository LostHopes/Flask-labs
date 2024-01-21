from flask import Blueprint

swagger = Blueprint("swagger", __name__)

from . import views, config