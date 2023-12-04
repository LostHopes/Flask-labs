from datetime import datetime

from app.feedback.models import Feedback
from app import db


class FeedbackHelper(Feedback):

    def show(self):
        feedbacks = Feedback.query.all()
        return feedbacks

    def add(self, comment, file, user_id):
        comment_date = datetime.now().replace(microsecond=0)
        feedback = Feedback(comment=comment, file=file, comment_date=comment_date, user_id=user_id)
        db.session.add(feedback)
        db.session.commit()

    def remove(self):
        pass

    def update(self):
        pass