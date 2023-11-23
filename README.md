# Лабораторна робота №5 WTF-форми

## 1. Форма входу

```
class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=16)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=16)])
    submit = SubmitField("Sign in", id="btn-signin")
```

## 2. Шаблон _fields.html

```
{% macro logout_form(form) %}
<div class="form-group p-2">
    {{ form.submit(class="btn btn-primary") }}
</div>
{% endmacro %}

{% macro login_form(form) %}
{{ form.csrf_token() }}
<div class="form-group p-2">
    {{ form.username.label }}
    {{ form.username(class="form-control") }}
</div>
<div class="form-group p-2">
    {{ form.password.label }}
    {{ form.password(class="form-control") }}
</div>
<div class="form-group p-2">
    {{ form.submit(class="btn btn-primary") }}
</div>

{% endmacro %}

{% macro change_password_form(form) %}
{{ form.csrf_token() }}
<div class="form-group p-2">
    {{ form.new_password.label }}
    {{ form.new_password(class="form-control") }}
</div>
<div class="form-group p-2">
    {{ form.repeat_password.label }}
    {{ form.repeat_password(class="form-control") }}
</div>
<div class="form-group p-2">
    {{ form.submit(class="btn btn-primary") }}
</div>

{% endmacro %}

{% macro add_cookies_form(form) %}
<div class="form-group p-2">
    {{ form.name.label }}
    {{ form.name(class="form-control") }}
</div>
<div class="form-group p-2">
    {{ form.value.label }}
    {{ form.value(class="form-control") }}
</div>
<div class="form-group p-2">
    {{ form.submit(class="btn btn-primary") }}
</div>

{% endmacro %}

{% macro rm_cookies_form(form) %}
<div class="form-group p-2">
    {{ form.name.label }}
    {{ form.name(class="form-control") }}
</div>
<div class="form-group p-2">
    {{ form.submit(class="btn btn-primary") }}
</div>

{% endmacro %}

{% macro todo_form(form) %}
<div class="form-group p-2">
    {{ form.task.label }}
    {{ form.task(class="border rounded form-control w-75") }}
</div>
<div class="form-group p-2">
    {{ form.save(class="btn btn-primary form-control w-auto") }}
</div>
{% endmacro %}
```

## 3. Перенаправлення на сторінку info при успішній авторизації

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
        return redirect(url_for("info"))
    return render_template("login.html", title=title, form=form)
```