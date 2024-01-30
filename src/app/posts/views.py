from flask import url_for, redirect, render_template, request, flash
from flask_login import login_required, current_user

from . import posts, helper
from .forms import WritePostForm, EditPostForm


@posts.route("/")
def show():
    title = "Posts"

    db = helper.PostsHelper()
    items = 9
    page = request.args.get("page", 1, type=int)
    pagination = db.show(page, items)

    image = url_for("static", filename="images/posts_thumbnails/default.jpg")
    return render_template("posts.html", title=title, pagination=pagination, image=image)


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

    db = helper.PostsHelper()
    post = db.get(id)

    form = EditPostForm()

    form.title.data = post.title
    form.text.data = post.text
    form.image.data = post.image

    if form.validate_on_submit():
        return redirect(url_for("posts.update"))


    return render_template("post_edit.html", title=title, form=form, id=id)


@posts.route("/", methods=["POST"])
@login_required
def create():

    db = helper.PostsHelper()

    db.create(
        request.form.get("title"),
        request.form.get("text"),
        request.form.get("category"),
        request.form.get("image"),
        current_user.get_id()
    )
    flash("Post was created", "success")
    return redirect(url_for("posts.show"))


@posts.route("/<int:id>")
def get(id):
    db = helper.PostsHelper()
    post = db.get(id)
    return render_template("article.html", post=post)


@posts.route("/update/<int:id>", methods=["POST"])
@login_required
def update(id):
    db = helper.PostsHelper()

    title = request.form.get("title")
    text = request.form.get("text")
    category = request.form.get("category")
    image = request.files.get("image")
    db.update(id, title, text, image, category)

    flash("Post was updated", "success")
    return redirect(url_for("posts.show"))


@posts.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    db = helper.PostsHelper()
    db.delete(id)
    flash("Post was deleted", "success")
    return redirect(url_for("posts.show"))
