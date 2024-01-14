from datetime import datetime

from app import db


class Films(db.Model):
    __tablename__ = "films"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date_out = db.Column(db.Date, nullable=False)
    time_added = db.Column(
        db.DateTime, nullable=False, 
        default=datetime.now().replace(second=0, microsecond=0)
    )
    genre = db.Column(db.String, nullable=False)
