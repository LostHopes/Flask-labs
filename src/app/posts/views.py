from flask import url_for, redirect, render_template
from flask_login import login_required, current_user

from app.helpers import posts_db
from . import posts


@posts.route("/list")
def posts_list():
    title = "Posts"
    return render_template("posts.html", title=title)

@posts.route("/create", methods=["POST"])
@login_required
def create():
    pass


@posts.route("/<int:id>")
def get_post(id=None):
    pass


@posts.route("/<int:id>/update", methods=["POST"])
@login_required
def update(id=None):
    pass


@posts.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id=None):
    pass
