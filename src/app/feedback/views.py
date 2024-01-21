from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from . import feedback, helper
from .forms import FeedbackForm


@feedback.route("/", methods=["GET", "POST"])
@login_required
def feedbacks():
    title = "Feedback"
    form = FeedbackForm()
    helper = helper.FeedbackHelper()
    comments = helper.show()

    if form.validate_on_submit():
        return redirect(url_for("feedback.add"))


    return render_template("feedback.html", title=title, form=form, comments=comments)


@feedback.route("/add", methods=["POST"])
@login_required
def add():
    db = helper.FeedbackHelper()
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
    
    db = helper.FeedbackHelper()
    db.remove(id)
    flash("Feedback was successfully deleted!", "success")
    
    return redirect(url_for("feedback.feedbacks"))


