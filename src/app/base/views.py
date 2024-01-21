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
    menu = [
        {"text": "Albums", "link": url_for("base.albums")},
        {"text": "Contact", "link": url_for("base.contact")},
        {"text": "Skills", "link": url_for("skills.show")},
        {"text": "Todo", "link": url_for("todo.todo_list")},
        {"text": "Posts", "link": url_for("posts.show")},
        {"text": "About", "link": url_for("base.about")},
        {"text": "Feedback", "link": url_for("feedback.feedbacks")},
    ]

    if current_user.is_anonymous:
        menu.extend([
            {"text": "Login", "link": url_for("user.login")},
            {"text": "Register", "link": url_for("user.register")}
        ])
    else:
        menu.append(
            {"text": "Account", "link": url_for("user.account")},
        )
    
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

    albums = [
        {
            "title": "The Night Shift",
            "artist": "Larry June",
            "url": "60hrxgJN3QfheGpVzEcUFR"
        },
        {
            "title": "Sunnasritual",
            "artist": "Kveld",
            "url": "49BaLxo4HMWHyGOHpEzuHD"
        },
        {
            "title": "And Then You Pray For Me",
            "artist": "Westside Gunn",
            "url": "3CXoPCQuBb7kP9vEFcfXKU"
        }
    ]

    return render_template("albums.html", title=title, albums=albums)


