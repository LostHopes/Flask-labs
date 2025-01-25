from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from app import config


app = Flask(__name__)

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()
api = Api()
login_manager.login_view = "user.login"
login_manager.login_message = "You should login before accessing this page"
login_manager.login_message_category = "info"


def create_app(config_class=config.DevConfig):
    from .base import base

    app.register_blueprint(base)

    from .user import user

    app.register_blueprint(user)

    from .todo import todo

    app.register_blueprint(todo, url_prefix="/todo")
    from .posts import posts

    app.register_blueprint(posts, url_prefix="/posts")

    from app.swagger import swagger

    app.register_blueprint(swagger, url_prefix="/api")

    from app.rest_api import rest_api

    app.register_blueprint(rest_api, url_prefix="/api")

    with app.app_context():
        app.config.from_object(config_class)
        db.init_app(app)
        migrate.init_app(app, db)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        db.create_all(bind_key=None)
        jwt.init_app(app)
        api.init_app(app)

    return app
