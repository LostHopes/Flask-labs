from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.feedback import feedback
from .forms import FeedbackForm
from app.helpers import feedback_db


@feedback.route("/", methods=["GET", "POST"])
@login_required
def feedbacks():
    title = "Feedback"
    form = FeedbackForm()
    helper = feedback_db.FeedbackHelper()
    comments = helper.show()

    if form.validate_on_submit():
        return redirect(url_for("feedback.add"))


    return render_template("feedback.html", title=title, form=form, comments=comments)


@feedback.route("/add", methods=["POST"])
@login_required
def add():
    db = feedback_db.FeedbackHelper()
    db.add(
        request.form.get("comment"),
        request.form.get("file"),
        current_user.get_id()
    )
    flash("Feedback added successfully!", "success")
    return redirect(url_for("feedback.feedbacks"))


@feedback.route("<int:id>/delete", methods=["POST"])
@login_required
def remove(id=None):
    
    db = feedback_db.FeedbackHelper()
    db.remove(id)
    flash("Feedback was successfully deleted!", "success")
    
    return redirect(url_for("feedback.feedbacks"))


