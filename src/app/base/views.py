from flask import render_template, url_for
from flask_login import current_user
import platform
import datetime

from app.base import base
from app import app


@app.context_processor
def links():
    now = datetime.datetime.now()
    time = now.strftime("%d/%m/%y %H:%M:%S")
    
    return dict(
        platform=platform,
        time=time
    )


@base.get("/")
def index():
    title = "Home"
    return render_template("index.html", title=title)


@base.get("/about")
def about():
    title = "About"
    return render_template("about.html", title=title)


@base.get("/contact")
def contact():
    title = "Contact"
    return render_template("contact.html", title=title)


