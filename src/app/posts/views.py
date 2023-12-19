from flask import url_for, redirect, render_template, request, flash
from flask_login import login_required, current_user

from app.helpers import posts_db
from .forms import WritePostForm, EditPostForm
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

    db = posts_db.PostsHelper()
    post = db.get(id)

    form = EditPostForm()

    form.title.data = post.title
    form.text.data = post.text

    if form.validate_on_submit():
        return redirect(url_for("posts.update"))


    return render_template("post_edit.html", title=title, form=form, id=id)


@posts.route("/create", methods=["POST"])
@login_required
def create():

    db = posts_db.PostsHelper()

    db.create(
        request.form.get("title"),
        request.form.get("text"),
        request.form.get("category"),
        current_user.get_id()
    )
    flash("Post was created", "success")
    return redirect(url_for("posts.show"))


@posts.route("/<int:id>")
def get(id):
    db = posts_db.PostsHelper()
    post = db.get(id)
    return render_template("article.html", post=post)


@posts.route("/update/<int:id>", methods=["POST"])
@login_required
def update(id):
    db = posts_db.PostsHelper()

    title = request.form.get("title")
    text = request.form.get("text")
    category = request.form.get("category")
    db.update(id, title, text, category)

    flash("Post was updated", "success")
    return redirect(url_for("posts.show"))


@posts.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    db = posts_db.PostsHelper()
    db.delete(id)
    flash("Post was deleted", "success")
    return redirect(url_for("posts.show"))
