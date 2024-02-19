from flask import render_template, redirect, url_for, flash, request
from sqlalchemy.exc import IntegrityError, StatementError
from PIL import UnidentifiedImageError
from flask_login import login_required, current_user, logout_user, login_user
import flask_jwt_extended as jwt

import datetime

from .forms import ChangePasswordForm, LoginForm, \
    LogoutForm, RegisterForm, UpdateAccountForm
from . import user, helper
from app import login_manager


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


    image_file = url_for("user.static", filename=f"images/profile_pics/{current_user.image}")
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
        db = helper.UsersHelper()
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


@user.route("/account/", methods=["POST"])
@login_required
def change_password():
    user = helper.UsersHelper()
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


@user.route("/register", methods=["GET"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("user.account"))

    title = "Register"
    form = RegisterForm()

    if form.validate_on_submit():
        return redirect(url_for("user.register_process"))

    return render_template("register.html", title=title, form=form)

@user.route("/register", methods=["POST"])
def register_process():

    user = helper.UsersHelper()
    register_date = datetime.datetime.now().replace(second=0, microsecond=0)

    try:    
        user.register(
            request.form.get("name"),
            request.form.get("surname"),
            request.form.get("login"), 
            request.form.get("email"), 
            request.form.get("password"),
            request.form.get("confirm_password"),
            register_date
        )
        flash("User was registered", "success")
        return redirect(url_for("user.login"))
    except IntegrityError:
        flash("User already exist", "danger")
        user.rollback()
        return redirect(url_for("user.register"))


@user.route("/login", methods=["GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("user.account"))

    title = "Login"
    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for("user.login_process"))
        
        
    return render_template("login.html", title=title, form=form)


@user.route("/login", methods=["POST"])
def login_process():
    user = helper.UsersHelper()

    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember")
    success = user.login(email, password)

    if not success:
        flash("Login failed", "danger")
        return redirect(url_for("user.login"))
    
    login_user(user.get_username(email), remember=remember)
    flash("Login successful", "success")
    return redirect(url_for("user.account"))


@user.route("/users")
@login_required
def users():
    handler = helper.UsersHelper()
    get_all = handler.get_all()
    return render_template("users.html", users=get_all)


@user.after_request
def after_request(response):
    now = datetime.datetime.now().replace(second=0, microsecond=0)
    current_user.last_seen = now
    try:
        db = helper.UsersHelper()
        db.commit()
    except StatementError:
        flash('Error while updating user last seen!', 'danger')
    return response

    