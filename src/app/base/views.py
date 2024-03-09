from flask import render_template, url_for
from flask_login import current_user
import platform
import datetime

from app.base import base
from app.base.helper import BaseHelper
from app import app


@app.context_processor
def links():
    now = datetime.datetime.now()
    time = now.strftime("%d/%m/%y %H:%M:%S")
    menu = BaseHelper.get_menu()
    
    return dict(
        platform=platform,
        time=time,
        menu=menu)


@base.route("/")
def index():
    title = "Home"
    return render_template("index.html", title=title)


@base.route("/about")
def about():
    title = "About"
    return render_template("about.html", title=title)


@base.route("/contact")
def contact():
    title = "Contact"
    return render_template("contact.html", title=title)


@base.route("/albums")
def albums():
    title="Albums"

    albums = BaseHelper.get_albums()

    return render_template("albums.html", title=title, albums=albums)


