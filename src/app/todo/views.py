from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.todo import helper, todo
from app.todo.forms import TodoForm


@todo.get("/")
@login_required
def todo_list():
    title = "Todo list"
    form = TodoForm()
    handle = helper.TodosHelper()
    todo = handle.show(current_user.get_id())

    return render_template("todo.html", title=title, form=form, todo=todo)


@todo.post("/")
@login_required
def add():

    try:
        todo = helper.TodosHelper()
        task = request.form.get("task")
        user_id = current_user.get_id()
        todo.add(task, user_id)
        flash("Task have been added to the list", "success")
    except IntegrityError:
        flash("Task with this name already exist", "danger")
        return redirect(url_for("todo.todo_list"))


    return redirect(url_for("todo.todo_list"))


@todo.post("<int:id>/delete/")
@login_required
def remove(id=None):

    todo = helper.TodosHelper()
    todo.remove(id)
    flash("Item was successfully removed from todo list", "success")

    return redirect(url_for("todo.todo_list"))


@todo.post("<int:id>/update/")
@login_required
def update(id=None):
    todo = helper.TodosHelper()
    todo.update(id)
    flash("Task was successfully updated", "success")
    return redirect(url_for("todo.todo_list"))