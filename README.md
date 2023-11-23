# Лабораторна робота No4 Об’єкт запиту request. Сесії та кукі.

## 1. Зміна розташування файлів:

![image](/screenshots/lab4/lab4_1.png)

## 2.1 Форма користувача і json файл з даними:

![image](/screenshots/lab4/lab4_2.png)

```
{"user": "admin", "password": "password"}
```

## 2.2 Перевірка автентифікації та перенаправлення користувача на сторінку info

```
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
```

## 2.3 Привітання користувача, який авторизувався

![image](/screenshots/lab4/lab4_3.png)

## 2.4 Вихід, зміна паролю, додавання та видалення cookie на сторінці info

![image](/screenshots/lab4/lab4_4.png)