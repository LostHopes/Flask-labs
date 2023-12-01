from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.helpers import todo_db
from . import todo
from .forms import TodoForm

_todo_list = "todo.todo_list"

@todo.route("/list")
@login_required
def todo_list():
    title = "Todo list"
    form = TodoForm()
    handle = todo_db.HandleTodos()
    todo = handle.show(current_user.get_id())

    return render_template("todo.html", title=title, form=form, todo=todo)


@todo.route("/add", methods=["POST"])
@login_required
def add():

    try:
        todo = todo_db.HandleTodos()
        task = request.form.get("task")
        user_id = current_user.get_id()
        todo.add(task, user_id)
        flash("Task have been added to the list", "success")
    except IntegrityError:
        flash("Task with this name already exist", "danger")
        return redirect(url_for(_todo_list))


    return redirect(url_for(_todo_list))


@todo.route("<int:id>/delete/", methods=["POST"])
@login_required
def remove(id=None):

    if id is not None:
        todo = todo_db.HandleTodos()
        todo.remove(id)
        flash("Item was successfully removed from todo list", "success")

    return redirect(url_for(_todo_list))


@todo.route("<int:id>/update/", methods=["POST"])
@login_required
def update(id=None):
    todo = todo_db.HandleTodos()
    todo.update(id)
    return redirect(url_for(_todo_list))
