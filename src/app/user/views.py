from flask import render_template, redirect, url_for, flash, request
from sqlalchemy.exc import IntegrityError, StatementError
from PIL import UnidentifiedImageError
from flask_login import login_required, current_user, logout_user, login_user

import datetime

from .forms import ChangePasswordForm, LoginForm, \
    LogoutForm, RegisterForm, UpdateAccountForm
from app.user import user
from app import login_manager
from app.helpers import user_db


@user.route("/account")
@login_required
def account():

    title = "Account"
    logout_form = LogoutForm()
    update_form = UpdateAccountForm()
    password_form = ChangePasswordForm()
    update_form.username.data = current_user.login
    update_form.email.data = current_user.email
    update_form.about.data = current_user.about
    # TODO: add response if user isn't active

    if update_form.validate_on_submit():
        return redirect(url_for("user.update_account"))

    if password_form.validate_on_submit():
        return redirect(url_for("user.change_password"))


    image_file = url_for("static", filename=f"images/profile_pics/{current_user.image}")
    return render_template(
        "account.html",
        title=title,
        logout_form=logout_form,
        update_form=update_form,
        password_form=password_form,
        image_file=image_file
    )


@user.route("/account/update", methods=["POST"])
@login_required
def update_account():
    try:
        db = user_db.HandleUsers()
        db.update(
            request.form.get("username"),
            request.form.get("email"),
            request.files.get("image"),
            request.form.get("about")
        )
        
        flash("Your account has been updated!", "success")
        return redirect(url_for("user.account"))

    except IntegrityError:
        flash("The user already exists", "danger")
        db.rollback()
        return redirect(url_for("user.account"))
    except UnidentifiedImageError:
        flash("Unsupported image format", "danger")
        return redirect(url_for("user.account"))


@user.route("/account/update/credentials", methods=["POST"])
@login_required
def change_password():
    user = user_db.HandleUsers()
    if user.change_password(
        request.form.get("new_password"),
        request.form.get("repeat_password")
        ):
        
        flash("Password changed!", "success")
        return redirect(url_for("user.account"))

    flash("Passwords isn't the same!", "danger")
    return redirect(url_for("user.account"))


@user.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", "success")
    return redirect(url_for("user.login"))


@user.route("/register", methods=["GET","POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("user.account"))

    try:
        title = "Register"
        form = RegisterForm()
        user = user_db.HandleUsers()
        
        register_date = datetime.datetime.now().replace(second=0, microsecond=0)
        if form.validate_on_submit():
            user.register(
                form.name.data,
                form.surname.data, 
                form.login.data, 
                form.email.data, 
                form.password.data,
                form.confirm_password.data,
                register_date
            )
            flash("User was registered", "success")
            return redirect(url_for("user.login"))
    except IntegrityError:
        flash("User already exist", "danger")
        user.rollback()
        return redirect(url_for("user.register"))
    
    return render_template("register.html", title=title, form=form)


@user.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("user.account"))

    title = "Login"
    form = LoginForm()
    user = user_db.HandleUsers()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        success = user.login(email, password)
        if success:
            login_user(user.get_username(email), remember=form.remember.data)
            flash("Login successful", "success")
            return redirect(url_for("user.account"))
        else:
            flash("Login failed", "danger")
            return redirect(url_for("user.login"))
        
    return render_template("login.html", title=title, form=form)


@user.route("/users")
@login_required
def users():
    handler = user_db.HandleUsers()
    get_all = handler.get_all()
    return render_template("users.html", users=get_all)


@user.after_request
def after_request(response):
    now = datetime.datetime.now().replace(second=0, microsecond=0)
    current_user.last_seen = now
    try:
        db = user_db.HandleUsers()
        db.commit()
    except StatementError:
        flash('Error while updating user last seen!', 'danger')
    return response

    