from app import db


class Skills(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)