from flask import url_for, redirect, render_template

from . import posts

@posts.route("/create", methods=["POST"])
def create():
    pass


@posts.route("/<int:id>")
def get_post(id=None):
    pass


@posts.route("/<int:id>/update", methods=["POST"])
def update(id=None):
    pass


@posts.route("/<int:id>/delete", methods=["POST"])
def delete(id=None):
    pass
