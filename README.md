# Лабораторна №11 CRUD. Публікація постів. Побудова зв'язків

# 1. CRUD Post

## 1.1 Модель Posts

| Column | Value |
| --- | --- |
| id | INTEGER(PK) |
| title | STRING |
| text | STRING |
| image | STRING |
| created_at | TIMESTAMP |
| category | ENUM |
| tags | relationship with PostsTag |
| enabled | BOOLEAN |
| user_id | FOREIGN KEY |

## 1.2 Маршрутизація в моделі Posts

### 1.2.1 Форма добавлення поста

#### 1.2.1.1 Сторінка написання

Вміст views.py блюпринта posts

```python
@posts.route("/write")
@login_required
def write():
    title = "Write post"

    form = WritePostForm()

    if form.validate_on_submit():
        return redirect(url_for("posts.create"))

    return render_template("post_write.html", title=title, form=form)
```

Форма створення посту файлу forms.py блюпринта posts

```python
class WritePostForm(FlaskForm):
    title = StringField("Post title", validators=[
        DataRequired(), Length(min=10, max=50)],
        render_kw={"placeholder": "Enter post title here:"})
    text = TextAreaField("Post content", validators=[
        DataRequired(), Length(min=250, max=5000)],
        render_kw={"cols": "50", "rows": "15", "placeholder": "Enter post content here:"})
    category = SelectField("Category", validators=[DataRequired()], choices=[("NEWS", "News"), ("PUBLICATIONS", "Publications"), ("OTHER", "Other")])
    submit = SubmitField("Publish")
```

HTML сторінка написання поста файлу post_write.html

```html
{% extends "base.html" %}
{% import "_fields.html" as field %}
{% block title %} {{ super() }} {% endblock %}
{% block content %}

<div class="d-flex justify-content-center gap-5 flex-wrap">
    <div class="flex-row align-items-center">
        <h1 class="title">Write post</h1>
    </div>
    <div class="flex-row">
        <div class="flex-column">
            <form action="{{ url_for('posts.create') }}" method="post">
                {{ field.write_post_form(form) }}
            </form>
        </div>
    </div>
</div>

{% endblock %}
```

#### 1.2.1.2 Обробка запиту POST створення поста

Допоміжна функція create у файлі posts_db.py

```python
def create(self, title, text, category, user_id):
        post = Posts(title=title, text=text, category=category, user_id=user_id)
        db.session.add(post)
        db.session.commit()
```

Вміст views.py блюпринта posts

```python
@posts.route("/create", methods=["POST"])
@login_required
def create():

    db = posts_db.PostsHelper()

    db.create(
        request.form.get("title"),
        request.form.get("text"),
        request.form.get("category"),
        current_user.get_id()
    )
    flash("Post was created", "success")
    return redirect(url_for("posts.show"))
```

### 1.2.2 Вивід всіх постів та пагінація

Допоміжна функція show у файлі posts_db.py

```python
def show(self, page, max_items):
    query = db.session.query(Posts, Users)\
        .join(Users).\
            order_by(Posts.created_at.desc())\
                .paginate(page=page, per_page=max_items)
    return query
```

Вміст views.py блюпринта posts

```python
@posts.route("/list")
def show():
    title = "Posts"

    db = posts_db.PostsHelper()
    items = 9
    page = request.args.get("page", 1, type=int)
    pagination = db.show(page, items)
    return render_template("posts.html", title=title, pagination=pagination)
```

HTML сторінка списку постів файлу posts.html

```html
{% extends "base.html" %}
{% block title %} {{ super() }} {% endblock %}
{% block content %}

<div class="container">
    {% include "_flashes.html" %}
    <div class="row">
        <div class="col">
            <h1 class="title text-center fs-1">Posts</h1>
        </div>
    </div>
    <div class="row p-5">
        <div class="col text-center">
            <form action="{{ url_for('posts.write') }}" method="get">
                <input type="submit" value="Write post" class="btn btn-primary">
            </form>
        </div>
    </div>
    <div class="row">
        {% for post, user in pagination.items %}
        <div class="col-md-4 p-3">
            <div class="text-center">
                <a href="{{ url_for('posts.get', id=post.id) }}">
                    {{ loop.index }} {{ post.title }}
                </a>
            </div>
            <div class="text-center"> Category: {{ post.category.value }}</div>
            <div class="text-center">Written by: {{ user.login }}</div>
            <div class="text-center">Created at: {{ post.created_at }}</div>

            {% if current_user.id == post.user_id %}
            <div class="d-flex justify-content-center p-2 gap-2">
                <form action="{{ url_for('posts.edit', id=post.id) }}" method="get">
                    <input type="submit" value="Edit" class="btn btn-primary">
                </form>
                <form action="{{ url_for('posts.delete', id=post.id) }}" method="post">
                    <input type="submit" value="Delete" class="btn btn-danger" 
                    onclick="return confirm('Are you sure you want to delete?')">
                </form>
            </div>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    <div class="pagination justify-content-center gap-3">
        {% if pagination.has_prev %}
            <a href="{{ url_for('posts.show', page=pagination.prev_num) }}">Previous</a>
        {% else %}
            <span class="disabled">Previous</span>
        {% endif %}
    
        {% if pagination.has_next %}
            <a href="{{ url_for('posts.show', page=pagination.next_num) }}">Next</a>
        {% else %}
            <span class="disabled">Next</span>
        {% endif %}
    </div>
    
</div>

{% endblock %}

```

### 1.2.3 Вивід одного поста

Допоміжна функція get у файлі posts_db.py

```python
def get(self, id):
    post = Posts.query.filter_by(id=id).first()
    return post
```

Вміст views.py блюпринта posts

```python
@posts.route("/<int:id>")
def get(id):
    db = posts_db.PostsHelper()
    post = db.get(id)
    return render_template("article.html", post=post)
```

HTML сторінка вибраного поста файлу article.html

```html
{% extends "base.html" %}
{% import "_fields.html" as field %}
{% block title %} {{ super() }} {% endblock %}
{% block content %}

<div class="container justify-content-center fs-4">
    <div>
        <h1 class="title p-5">{{ post.title }}</h1>
    </div>
    <div>
        <p>{{ post.text }}</p>
    </div>
    <div>
        <p>Published at: {{ post.created_at }}</p>
    </div>
</div>

{% endblock %}
```

### 1.2.4 Оновлення існуючого поста

#### 1.2.4.1 Сторінка оновлення

Вміст views.py блюпринта posts

```python
@posts.route("/edit/<int:id>")
@login_required
def edit(id):
    title = "Edit post"

    db = posts_db.PostsHelper()
    post = db.get(id)

    form = EditPostForm()

    form.title.data = post.title
    form.text.data = post.text

    if form.validate_on_submit():
        return redirect(url_for("posts.update"))


    return render_template("post_edit.html", 
    title=title, form=form, id=id)
```

Форма оновлення посту файлу forms.py блюпринта posts

```python
class EditPostForm(FlaskForm):
    title = StringField("Post title", validators=[DataRequired(), Length(min=10, max=50)], render_kw={"placeholder": "Enter post title here:"})
    text = TextAreaField("Post content", validators=[
        DataRequired(), Length(min=250, max=5000)],
        render_kw={"cols": "50", "rows": "15", "placeholder": "Enter post content here:"})
    category = SelectField("Category", validators=[DataRequired()], choices=[("NEWS", "News"), ("PUBLICATIONS", "Publications"), ("OTHER", "Other")])
    submit = SubmitField("Edit")
```

HTML сторінка оновлення вибраного поста файлу post_edit.html

```html
{% extends "base.html" %}
{% import "_fields.html" as field %}
{% block title %} {{ super() }} {% endblock %}
{% block content %}

<div class="d-flex justify-content-center gap-5 flex-wrap">
    <div>
        <h1 class="title">Edit post</h1>
    </div>
    <div>
        <form action="{{ url_for('posts.update', id=id) }}" method="post">
            {{ field.edit_post_form(form) }}
        </form>
    </div>
</div>

{% endblock %}
```

#### 1.2.4.2 Обробка запиту POST оновлення

Допоміжна функція update у файлі posts_db.py

```python
def update(self, id, title, text, category):
    post = Posts.query.filter_by(id=id).first()
    post.title = title
    post.text = text
    post.category = category
    db.session.commit()
```

Вміст views.py блюпринта posts

```python
@posts.route("/update/<int:id>", methods=["POST"])
@login_required
def update(id):
    db = posts_db.PostsHelper()

    title = request.form.get("title")
    text = request.form.get("text")
    category = request.form.get("category")
    db.update(id, title, text, category)

    flash("Post was updated", "success")
    return redirect(url_for("posts.show"))
```

### 1.2.5 Видалення поста

Допоміжна функція delete у файлі posts_db.py

```python
def delete(self, id):
    post = Posts.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
```

Вміст views.py блюпринта posts

```python
@posts.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    db = posts_db.PostsHelper()
    db.delete(id)
    flash("Post was deleted", "success")
    return redirect(url_for("posts.show"))
```

# 2. Візуальне представлення блюпринта post

## 2.1 Створення

![image](/screenshots/lab11/lab11_1.png)

## 2.2 Відображення всіх постів

### 2.2.1 Від автора

![image](/screenshots/lab11/lab11_2.png)

### 2.2.2 Від читача

![image](/screenshots/lab11/lab11_7.png)

## 2.3 Відображення Одного поста

![image](/screenshots/lab11/lab11_3.png)

## 2.4 Редагування

![image](/screenshots/lab11/lab11_4.png)

## 2.5 Видалення

Підтверження видалення поста

![image](/screenshots/lab11/lab11_5.png)

Результат видалення

![image](/screenshots/lab11/lab11_6.png)




