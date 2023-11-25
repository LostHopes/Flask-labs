from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from app import config
from app import app
from app.config import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default="Planning", nullable=False)
    category = db.Column(db.String, default="Empty", nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Skills(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
 
    
# TODO: add user comments!