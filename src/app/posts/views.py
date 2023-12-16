from flask import url_for, redirect, render_template, request
from flask_login import login_required, current_user

from app.helpers import posts_db
from .forms import WritePostForm
from . import posts


@posts.route("/list")
def show():
    title = "Posts"

    db = posts_db.PostsHelper()
    posts = db.show()

    return render_template("posts.html", title=title, posts=posts)


@posts.route("/write")
@login_required
def write():
    title = "Write post"

    form = WritePostForm()

    if form.validate_on_submit():
        return redirect(url_for("posts.create"))

    return render_template("post_write.html", title=title, form=form)


@posts.route("/edit/<int:id>")
@login_required
def edit(id):
    title = "Edit post"
    return render_template("post_edit.html", title=title)


@posts.route("/create", methods=["POST"])
@login_required
def create():

    db = posts_db.PostsHelper()

    db.create(
        request.form.get("title"),
        request.form.get("text"),
        current_user.get_id()
    )

    return redirect(url_for("posts.show"))


@posts.route("/<int:id>")
def get(id=None):
    pass


@posts.route("/<int:id>/update", methods=["POST"])
@login_required
def update(id=None):
    pass


@posts.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    db = posts_db.PostsHelper()
    db.delete(id)
    return redirect(url_for("posts.show"))
