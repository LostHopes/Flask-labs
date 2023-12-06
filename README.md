# Самостійна робота: відгуки користувачів

## 1. Компоненти блюпринта feedback

### 1.1 Таблиця в базі даних

Вміст файлу *models.py* блюпринта feedback

```python
from app import db


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    comment = db.Column(db.Text, nullable=False)
    file = db.Column(db.Text, default=None)
    comment_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
```

Для можливості додавати дані з інших таблиць (JOIN), ми створюємо зв'язок у моделі Users (див. Завдання 2)[#2]

Вміст файлу *models.py* блюпринта user

```python
feedbacks = db.relationship("Feedback", backref="author", lazy=True)
```

### 1.2 Форма додавання відгуків

Вміст файлу *forms.py* блюпринта feedback

```python
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length
from wtforms import TextAreaField, SubmitField


class FeedbackForm(FlaskForm):
    comment = TextAreaField("Text", validators=[DataRequired(), Length(min=40)])
    file = FileField("File", validators=[FileAllowed(["jpg", "png"], "Images only!")])
    submit = SubmitField("Publish")
```

### 1.3 Маршрут feedback

Користувач може добавляти, видаляти відгук, написаний ним; а також переглядати відгуки інших користувачів

Вміст файлу *views.py* блюпринта feedback

```python
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.helpers import todo_db
from . import todo
from .forms import TodoForm


@todo.route("/list")
@login_required
def todo_list():
    title = "Todo list"
    form = TodoForm()
    handle = todo_db.TodosHelper()
    todo = handle.show(current_user.get_id())

    return render_template("todo.html", title=title, form=form, todo=todo)


@todo.route("/add", methods=["POST"])
@login_required
def add():

    try:
        todo = todo_db.TodosHelper()
        task = request.form.get("task")
        user_id = current_user.get_id()
        todo.add(task, user_id)
        flash("Task have been added to the list", "success")
    except IntegrityError:
        flash("Task with this name already exist", "danger")
        return redirect(url_for("todo.todo_list"))


    return redirect(url_for("todo.todo_list"))


@todo.route("<int:id>/delete/", methods=["POST"])
@login_required
def remove(id=None):

    todo = todo_db.TodosHelper()
    todo.remove(id)
    flash("Item was successfully removed from todo list", "success")

    return redirect(url_for("todo.todo_list"))


@todo.route("<int:id>/update/", methods=["POST"])
@login_required
def update(id=None):
    todo = todo_db.TodosHelper()
    todo.update(id)
    return redirect(url_for("todo.todo_list"))
```

## 2. Допоміжні функції

Допоміжні функції знаходяться у віддільному файлі. 
В ньому є функції додавання, видалення, перегляду відгуків.

Вміст *feedback_db.py*

```python
from datetime import datetime

from app.user.models import Users
from app.feedback.models import Feedback
from app import db


class FeedbackHelper(Feedback):

    def show(self):
        feedbacks = db.session.query(Feedback, Users).join(Users).all()
        return feedbacks

    def add(self, comment, file, user_id):
        comment_date = datetime.now().replace(microsecond=0)
        feedback = Feedback(comment=comment, file=file, comment_date=comment_date, user_id=user_id)
        db.session.add(feedback)
        db.session.commit()

    def remove(self, id):
        comment = Feedback.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()


    def update(self):
        pass
```

## 3. HTML сторінка та її представлення у браузері

Вміст файлу *feedback.html*

```html
{% extends "base.html" %}
{% block title %} {{ super() }} {% endblock %}
{% import "_fields.html" as field %}

{% block content %}

<div class="d-flex justify-content-center flex-wrap col-md-6 mx-auto">
    <div class="flex-row w-100">
        <h1 class="title p-3 text-center w-100">Feedback</h1>
    </div>
    <div>
        {% include "_flashes.html" %}
        {% for comment, user in comments %}
        <div>{{ comment.comment }}</div>
        <div class="pt-3">Published in: {{ comment.comment_date }}</div>
        <div class="pt-3">Published by: {{ user.login }}</div>
        <div class="d-flex pb-5 gap-2">
            {% if current_user.id == comment.user_id %}
            <div class="flex-row py-2">
                <form action="{{ url_for('feedback.remove', id=comment.id) }}" method="post">
                    <input type="submit" value="Remove" class="btn btn-danger">
                </form>
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    <div class="flex-row">
        <div>
            <form action="{{ url_for('feedback.add') }}" method="post" enctype="multipart/form-data">
                {{ field.feedback_form(form) }}
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

Додавання відгуку

![image](/screenshots/feedback/feedback_1.png)

Видалення відкугу

![image](/screenshots/feedback/feedback_2.png)

Перегляд відгуку від іншого користувача

![image](/screenshots/feedback/feedback_3.png)




