import os
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Database connection
basedir = basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db/users.sqlite")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# session key
app.secret_key = b"secretkey123"