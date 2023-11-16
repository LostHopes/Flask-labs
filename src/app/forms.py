from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LogoutForm(FlaskForm):
    submit = SubmitField("Logout", id="btn-logout")


class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=16)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=16)])
    submit = SubmitField("Sign in", id="btn-signin")


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=4, max=16)])
    repeat_password = PasswordField("Repeat new password", validators=[DataRequired(), Length(min=4, max=16)])
    submit = SubmitField("Change Password", id="btn-chpasswd")


class CookiesForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=16)])
    value = StringField("Value", validators=[DataRequired(), Length(min=4, max=50)])
    submit = SubmitField("Modify cookie", id="cookies")


class TodoForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Enter a task here"})
    save = SubmitField("Save")