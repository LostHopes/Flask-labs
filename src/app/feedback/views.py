from flask import render_template

from app.feedback import feedback


@feedback.route("/feedback/")
def feedbacks():
    title = "Feedback"
    return render_template("feedback.html", title=title)