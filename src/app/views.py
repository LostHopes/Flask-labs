from flask import request, render_template, redirect, url_for, session, flash, make_response
from flask_bcrypt import check_password_hash
import platform
import datetime
from sqlalchemy.exc import IntegrityError

from data import data
from app import app
from .api.skills import get_skills
from app.forms import LoginForm, RegisterForm, ChangePasswordForm, CookiesForm, LogoutForm, TodoForm
from app.helpers import database


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
        {"text": "Register", "link": url_for("register")},
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


@app.route("/skills/")
@app.route("/skills/<int:s_id>/")
def skills(s_id=None):
    title = "My skills"
    if s_id is not None:
        title = title.rstrip("s")
    my_skills = data.my_skills
    return render_template("skills.html", title=title, my_skills=my_skills, s_id=s_id)


@app.route("/register", methods=["GET","POST"])
def register():
    try:
        title = "Register"
        form = RegisterForm()
        user = database.HandleUsers()
        
        if form.validate_on_submit():
            user.register(
                form.name.data,
                form.surname.data, 
                form.login.data, 
                form.email.data, 
                form.password.data,
                form.confirm_password.data
            )
            flash("User was registered", "success")
            return redirect(url_for("login"))
    except IntegrityError:
        flash("User already exist", "danger")
        return redirect(url_for("register"))
    
    return render_template("register.html", title=title, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    
    title = "Login"
    form = LoginForm()
    user = database.HandleUsers()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        info = user.login(email, password)
        if info.email == email and check_password_hash(info.password, password):
            flash("Login successful", "success")
            return redirect(url_for("profile"))
        else:
            flash("Login failed", "danger")
            return redirect(url_for("login"))
        
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
            flash("Password changed successfully", "success")
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


@app.route("/cookie/add/", methods=["POST"])
def add_cookie():
    name = request.form.get("name")
    value = request.form.get("value")
    expire_date = datetime.datetime.now() + datetime.timedelta(days=1)

    response = make_response(redirect(url_for("info")))

    if name in request.cookies:
        flash(f"Cookie with name {name} already exist", "warning")
        return response

    response.set_cookie(name, value, expires=expire_date)
    flash(f"You successfully added cookie {name} that expires in {expire_date.date()}", "success")
        
    return response


@app.route("/cookie/remove/", methods=["POST"])
def remove_cookie():
    response = make_response(redirect(url_for("info")))
    name = request.form.get("name")

    if name not in request.cookies:
        flash(f"Cookie with name {name} doesn't exist", "warning")
        return response

    response.delete_cookie(name)
    flash(f"You successfully removed cookie {name}", "success")
    return response


@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    flash("You successfully logged out", "success")
    return redirect(url_for("index"))


@app.route("/todo")
def todo_list():
    title = "Todo list"
    form = TodoForm()
    handle = database.HandleTodos()
    todo = handle.show()

    return render_template("todo.html", title=title, form=form, todo=todo)


@app.route("/todo/add/", methods=["POST"])
def add_todo():

    try:
        todo = database.HandleTodos()
        todo.add(request.form.get("task"))
        flash("Task have been added to the list", "success")
    except IntegrityError:
        flash("Task with this name already exist", "danger")
        return redirect(url_for("todo_list"))


    return redirect(url_for("todo_list"))


@app.route("/todo/<int:id>/delete/", methods=["POST"])
def remove_todo(id=None):

    if id is not None:
        todo = database.HandleTodos()
        todo.remove(id)
        flash("Item was successfully removed from todo list", "success")

    return redirect(url_for("todo_list"))


@app.route("/todo/<int:id>/update/", methods=["POST"])
def update_todo(id=None):
    todo = database.HandleTodos()
    todo.update(id)
    return redirect(url_for("todo_list"))


@app.route("/feedback/")
def feedback():
    title = "Feedback"
    return render_template("feedback.html", title=title)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    title = "Profile"
    return render_template("profile.html", title=title)