from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db", "users.sqlite")

app.secret_key = b"secretkey123"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "user.login"
login_manager.login_message = "You should login before accessing this page"
login_manager.login_message_category = "info"

from .user import user
app.register_blueprint(user, url_prefix="/user")

from .todo import todo
app.register_blueprint(todo, url_prefix="/todo")

from .cookies import cookies
app.register_blueprint(cookies, url_prefix="/cookies")

from .skills import skills
app.register_blueprint(skills, url_prefix="/skills")

from . import views
   