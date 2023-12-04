from app import db


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    comment = db.Column(db.Text, nullable=False)
    file = db.Column(db.Text, default=None)
    comment_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)