# Лабораторна №9 Профіль користувача

## 1. Модель користувача Users

Вміст файлу *models.py*
```python
class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default.jpg")
    last_seen = db.Column(db.DateTime, default=datetime.now().replace(second=0, microsecond=0))
    about = db.Column(db.Text , default="", nullable=False)
    register_date = db.Column(db.DateTime, nullable=False)
```

## 2. Фото за замовчуванням

Вміст файлу *models.py*
```python
image = db.Column(db.String(20), nullable=False, default="default.jpg")
```

Візуальне представлення сторінки *account*

![image](/screenshots/lab9/lab9_1.png)

## 3. Форма для оновлення даних користувача

![image](/screenshots/lab9/lab9_2.png)

Валідація здійснюється за допогою обробки помилки *IntegrityError* з бібліотеки SQLAlchemy

Вміст файлу *views.py*, роута login
```python
except IntegrityError:
    flash("The user already exists", "danger")
    db.rollback()
    return redirect(url_for("account"))
```

Візуальне представлення сторінки *account*

![image](/screenshots/lab9/lab9_3.png)

## 4. Поточні значення користувача в формі

Візуальне представлення сторінки *account*

![image](/screenshots/lab9/lab9_4.png)

Дані користувача з бази даних

![image](/screenshots/lab9/lab9_5.png)

## 5. Фото профілю

В функції save_picture я використовую метод бібліотеки Pillow для зміни розміру розбраження - resize,
а також secrets для генерації назви файлу

Вміст файлу з допоміжними функціями *database.py*

```python
@staticmethod
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.split(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, "static", "images", "profile_pics", picture_filename)
    image = Image.open(form_picture)
    new_image = image.resize((300, 300))
    new_image.save(picture_path)
    return picture_filename


def update(self, username, email, image, about):

    current_user.login = username
    current_user.email = email

    if image:
        current_user.image = self.save_picture(image)

    current_user.about = about


    self.commit()
```

Візуальне представлення сторінки *account*

![image](/screenshots/lab9/lab9_6.png)

## 6. Поля about, last_seen

Вміст файлу *models.py* [(див. Завдання №1)](#1-модель-користувача-users)

Візуальне представлення сторінки *account* [(див. Завдання №2)](#2-фото-за-замовчуванням) та [(див. Завдання №3)](#3-форма-для-оновлення-даних-користувача)

## 7. Зміна пароля користувача у профілі

Вміст файлу *views.py*

```python
@app.route("/account/update/credentials", methods=["POST"])
@login_required
def change_password():
    user = database.HandleUsers()
    if user.change_password(
        request.form.get("new_password"),
        request.form.get("repeat_password")
        ):
        
        flash("Password changed!", "success")
        return redirect(url_for("account"))

    flash("Passwords isn't the same!", "danger")
    return redirect(url_for("account"))
```

Допомоміжна функція change_password з файлу *database.py*

```python
def change_password(self, new_password, repeat_password):
    succeed = False
    
    validation = new_password == repeat_password

    if validation:
        password_hash = generate_password_hash(new_password)
        current_user.password = password_hash
        db.session.commit()
        succeed = True
        return succeed

    return succeed
```

Візуальне представлення сторінки *account*

![image](/screenshots/lab9/lab9_7.png)

Спроба змінити пароль, якщо вони не співпадають

![image](/screenshots/lab9/lab9_8.png)
