from flask import request, render_template, redirect, url_for, session, flash, make_response
import platform
import datetime
from data import data
from app import app
from .api.skills import get_skills
from app.forms import UserForm, ChangePasswordForm, CookiesForm, LogoutForm, TodoForm
from app.config import db
from app.functions import database


@app.context_processor
def base():
    now = datetime.datetime.now()
    time = now.strftime("%d/%m/%y %H:%M:%S")
    menu = [
        {"text": "Albums", "link": url_for("albums")},
        {"text": "Contact", "link": url_for("contact")},
        {"text": "Skills", "link": url_for("skills")},
        {"text": "Todo", "link": url_for("todo_list")},
        {"text": "About", "link": url_for("about")},
        {"text": "Feedback", "link": url_for("feedback")},
        {"text": "Login", "link": url_for("login")},
    ]
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
    return render_template("albums.html", title=title)


@app.route("/skills/")
@app.route("/skills/<int:s_id>/")
def skills(s_id=None):
    title = "My skills"
    if s_id is not None:
        title = title.rstrip("s")
    my_skills = data.my_skills
    return render_template("skills.html", title=title, my_skills=my_skills, s_id=s_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("info"))
    
    title = "Login"
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        auth = data.auth()
        if auth["user"] != username or auth["password"] != password:
            flash("Login incorrect", "danger")
            return render_template("login.html", title=title, form=form)
        session['username'] = username
        return redirect(url_for("info")) # changed from index to profile
    return render_template("login.html", title=title, form=form)


@app.route("/info", methods=["GET", "POST"])
def info():
    if "username" not in session:
        return redirect(url_for("login"))

    title = "Info"

    logout_form = LogoutForm()

    password_form = ChangePasswordForm()
    if password_form.validate_on_submit():
        new_password = password_form.new_password.data
        repeat_password = password_form.repeat_password.data
        if new_password == repeat_password:
            data.auth(session["username"], new_password)

    cookies_form = CookiesForm()
    cookies = request.cookies

    return render_template(
        "info.html",
        title=title,
        logout_form=logout_form,
        password_form=password_form,
        cookies_form=cookies_form,
        cookies=cookies)


@app.route("/cookie/", methods=["POST"])
@app.route("/add/", methods=["POST"])
def add_cookie():
    name = request.form.get("name")
    value = request.form.get("value")

    expire_date = datetime.datetime.now() + datetime.timedelta(days=1)

    response = make_response(redirect(url_for("profile")))
    response.set_cookie(name, value, expires=expire_date)
        
    return response


@app.route("/cookie/", methods=["POST"])
@app.route("/remove/", methods=["POST"])
def remove_cookie():
    response = make_response(redirect(url_for("profile")))
    name = request.form.get("name")
    response.delete_cookie(name)

    return response


@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for("index"))


@app.route("/todo")
def todo_list():
    title = "Todo list"
    form = TodoForm()

    return render_template("todo.html", title=title, form=form)


@app.route("/todo/", methods=["POST"])
@app.route("/add/", methods=["POST"])
def add_todo():

    

    return redirect(url_for("todo_list"))


@app.route("/todo/", methods=["POST"])
@app.route("/remove/", methods=["POST"])
def remove_todo():
    return redirect(url_for("todo_list"))


@app.route("/todo/", methods=["POST"])
@app.route("/update/", methods=["POST"])
def update_todo():
    return redirect(url_for("todo_list"))


@app.route("/feedback/")
def feedback():
    title = "Feedback"
    return render_template("feedback.html", title=title)


@app.route("/profile")
def profile():
    return