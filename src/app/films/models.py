from app import db


class Films(db.Model):
    __tablename__ = "films"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    date_out = db.Column(db.Date, nullable=False)
    time_added = db.Column(db.DateTime, nullable=False)
    genre = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
