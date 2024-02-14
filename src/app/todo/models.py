from enum import Enum

from app import db


class TodoPriority(Enum):
    LOW = "Low"
    MID = "Medium"
    HIGH = "High"


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default="Planning", nullable=False)
    category = db.Column(db.String, default="Empty", nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)