from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from app import config
from app import app
from app.config import db


# TODO: add flask-migration

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(16), nullable=False)
    surname = db.Column(db.String(16), nullable=False)

    def __init__(self):
        pass

    def __repr__(self):
        return


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    task_name = db.Column(db.Text, nullable=False)
    task_status = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# TODO: add user comments!