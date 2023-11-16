import os
from app import app
from flask_sqlalchemy import SQLAlchemy

# Database connection
basedir = basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "instance/users.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# session key
app.secret_key = b"secretkey123"