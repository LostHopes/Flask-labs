from app import db


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    file = db.Column(db.Text, nullable=False, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)