from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from .data import data
from . import skills

@skills.route("/")
@skills.route("/<int:id>/")
def show(id=None):
    title = "My skills"
    if id is not None:
        title = title.rstrip("s")
    my_skills = data.my_skills
    return render_template("skills.html", title=title, my_skills=my_skills, id=id)
