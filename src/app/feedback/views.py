from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app.feedback import feedback
from .forms import FeedbackForm
from app.helpers import feedback_db


@feedback.route("/", methods=["GET", "POST"])
@login_required
def feedbacks():
    title = "Feedback"
    form = FeedbackForm()

    if form.validate_on_submit():
        return redirect(url_for("feedback.add"))


    return render_template("feedback.html", title=title, form=form)


@feedback.route("/add", methods=["POST"])
@login_required
def add():
    return redirect(url_for("feedback.feedbacks"))


@feedback.route("/remove", methods=["POST"])
@login_required
def remove():
    return redirect(url_for("feedback.feedbacks"))


