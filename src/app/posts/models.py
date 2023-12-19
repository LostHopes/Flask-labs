import enum
from datetime import datetime

from app import db

class PostType(enum.Enum):
    NEWS = "News"
    PUBLICATIONS = "Publications"
    OTHER = "Other"


class Posts(db.Model):
    _tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String, nullable=False, default="postdefault.jpg")
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now().replace(microsecond=0))
    category = db.Column(db.Enum(PostType), nullable=False, default=PostType.NEWS)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class PostsCategory(db.Model):
    __tablename__ = "posts_category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class PostsTag(db.Model):
    __tablename__ = "posts_tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
