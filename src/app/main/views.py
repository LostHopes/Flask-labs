from flask import request, render_template, redirect, url_for, session, flash, make_response
from flask_bcrypt import check_password_hash
from flask_login import current_user
import platform
import datetime
from sqlalchemy.exc import IntegrityError, StatementError
from PIL import UnidentifiedImageError

from app import app
from app.helpers import database

@app.context_processor
def base():
    now = datetime.datetime.now()
    time = now.strftime("%d/%m/%y %H:%M:%S")
    menu = [
        {"text": "Albums", "link": url_for("albums")},
        {"text": "Contact", "link": url_for("contact")},
        {"text": "Skills", "link": url_for("skills.skills_list")},
        {"text": "Todo", "link": url_for("todo.todo_list")},
        {"text": "About", "link": url_for("about")},
        {"text": "Feedback", "link": url_for("user.feedback")},
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


@app.route("/")
def index():
    title = "Home"
    return render_template("index.html", title=title)


@app.route("/about")
def about():
    title = "About"
    return render_template("about.html", title=title)


@app.route("/contact")
def contact():
    title = "Contact"
    return render_template("contact.html", title=title)


@app.route("/albums")
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


