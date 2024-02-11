import enum
from datetime import datetime

from app import db

class PostType(enum.Enum):
    NEWS = "News"
    PUBLICATIONS = "Publications"
    OTHER = "Other"


class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String, nullable=False, default="default.jpg")
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now().replace(microsecond=0))
    category = db.Column(db.Enum(PostType), nullable=False, default=PostType.NEWS)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tags = db.relationship("PostsTags", backref="tags", lazy="dynamic", cascade="all, delete")


class PostsTags(db.Model):
    __tablename__ = "posts_tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
