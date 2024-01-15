from flask_login import UserMixin

from datetime import datetime

from app import app,db


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
    last_seen = db.Column(db.DateTime, default=datetime.now().replace(second=0, microsecond=0))
    about = db.Column(db.Text , default="", nullable=False)
    register_date = db.Column(db.DateTime, nullable=False)
    feedbacks = db.relationship("Feedback", backref="author", lazy=True)