# Лабораторна №8 Управління сеансами користувачів для зареєстрованих користувачів.Flask-Login

## 1. Ініціалізація LoginManager

Вміст файлу *config.py*

```python
import os
from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Database connection
basedir = basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db/users.sqlite")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


# session key
app.secret_key = b"secretkey123"
```

## 2. Імплементація is_authenticated, is_active, is_anonymous, get_id та user_loader

Вміст файлу *views.py*

### 2.1 is_authenticated

```python
if current_user.is_authenticated:
    return redirect(url_for("account"))
```

### 2.2 is_active

```python
if current_user.is_active:
    form = LogoutForm()
    return render_template("account.html", title=title, form=form)
```

### 2.3 is_anonymous

```python
if current_user.is_anonymous:
    menu.extend([
        {"text": "Login", "link": url_for("login")},
        {"text": "Register", "link": url_for("register")}
    ])
else:
    menu.append(
        {"text": "Account", "link": url_for("account")},
    )
```

### 2.4 get_id

```python
todo = database.HandleTodos()
task = request.form.get("task")
user_id = current_user.get_id()
todo.add(task, user_id)
flash("Task have been added to the list", "success")
```

### 2.5 user_loader

Вміст файлу *database.py*

```python
@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)
```

## 3. Реєстрація сеансу користувача

Вміст файлу *views.py*

```python
login_user(user.get_username(email), remember=form.remember.data)
flash("Login successful", "success")
return redirect(url_for("account"))
```

Автентифікація користувача здійснюється за допомогою допоміжного методу get_username, 
який повертає екземпляр класу в файлі *database.py*

```python
def get_username(self, email):
    username = db.session.query(Users).filter_by(email=email).first()
    return username
```

## 4. Об'єкт поточного користувача

Вміст файлу *views.py*

```python
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/register", methods=["GET","POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("account"))

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

    if current_user.is_authenticated:
        return redirect(url_for("account"))

    title = "Login"
    form = LoginForm()
    user = database.HandleUsers()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        success = user.login(email, password)
        if success:
            login_user(user.get_username(email), remember=form.remember.data)
            flash("Login successful", "success")
            return redirect(url_for("account"))
        else:
            flash("Login failed", "danger")
            return redirect(url_for("login"))
        
    return render_template("login.html", title=title, form=form)

```

## 5. Реалізація виходу користувача з сеансу

**Форма виходу добавлена на сторінці account, як альтернативне дизайн рішення**

Вміст файлу *views.py*

```python
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", "success")
    return redirect(url_for("login"))
```

Візуальне представлення сторінки *account*

![image](/screenshots/lab8/lab8_1.png)

## 6. Меню реєстрації, входу та виходу [(див. Завдання №2.3)](#23-is_anonymous)

## 7. Маршрут *account*, його шаблон та меню

### 7.1 Маршрут *account*

Вміст файлу *views.py*

```python
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    title = "Account"

    if current_user.is_active:
        form = LogoutForm()
        return render_template("account.html", title=title, form=form)


    return render_template("account.html", title)
```

### 7.2 Шаблон *account*

Вміст файлу *account.html*

```html
{% extends "base.html" %}
{% import "_fields.html" as field %}
{% block title %} {{ super() }} {% endblock %}
{% block content %}

<div class="col-lg-12 border rounded-5 p-5">
    {% include "_flashes.html" %}
    <div class="container text-center form-group py-5">
        <h2>Account info</h2>
        <div class="container py-2">
            User: {{ current_user.login }}
            <form action="{{ url_for('logout') }}" method="post">
                {{ field.logout_form(form) }}
            </form>
        </div>
        <div class="p-2">
           Email: {{ current_user.email }}
        </div>
        <div class="col-lg-8 offset-lg-2">
            <div class="form-group">
              <label for="about">About me</label>
              <textarea id="about" name="about" class="form-control" rows="3"></textarea>
            </div>
          </div>
    </div>
</div>

{% endblock %}
```

### 7.3 Сеанс користувача та меню

Меню до входу

![image](/screenshots/lab8/lab8_2.png)

Меню після входу

![image](/screenshots/lab8/lab8_3.png)

## 8. Декоратор login_required [(див. Завдання №7.1)](#71-маршрут-account)

## 9. Атрибут login_view

[див. Завдання №1](#1-ініціалізація-loginmanager)

Після додавання *login_view* і *login_message_category* 
перша - перенаправляє користувача на сторінку автентифікації,
друга - надсилає flash повідомлення з категорією *info*

Результат ініціалізації атрибута *login_view*

![image](/screenshots/lab8/lab8_4.png)