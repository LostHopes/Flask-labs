from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, make_response, flash
import datetime

from .forms import CookiesForm
from . import cookies


@cookies.route("/", methods=["GET"])
@login_required
def info():
    if current_user.is_anonymous:
        return redirect(url_for("user.login"))

    title = "Info"

    cookies_form = CookiesForm()
    cookies = request.cookies

    return render_template(
        "info.html",
        title=title,
        cookies_form=cookies_form,
        cookies=cookies)


@cookies.route("/", methods=["POST"])
def add():
    name = request.form.get("name")
    value = request.form.get("value")
    expire_date = datetime.datetime.now() + datetime.timedelta(days=1)

    response = make_response(redirect(url_for("cookies.info")))

    if name in request.cookies:
        flash(f"Cookie with name {name} already exist", "warning")
        return response

    response.set_cookie(name, value, expires=expire_date)
    flash(f"You successfully added cookie {name} that expires in {expire_date.date()}", "success")
        
    return response


@cookies.route("/remove/", methods=["POST"])
def remove():
    response = make_response(redirect(url_for("cookies.info")))
    name = request.form.get("name")

    if name not in request.cookies:
        flash(f"Cookie with name {name} doesn't exist", "warning")
        return response

    response.delete_cookie(name)
    flash(f"You successfully removed cookie {name}", "success")
    return response