from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from .data import data
from . import skills

@skills.route("/skills/")
@skills.route("/skills/<int:s_id>/")
def s_list(s_id=None):
    title = "My skills"
    if s_id is not None:
        title = title.rstrip("s")
    my_skills = data.my_skills
    return render_template("skills.html", title=title, my_skills=my_skills, s_id=s_id)
