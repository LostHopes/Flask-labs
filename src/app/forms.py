from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired, Length


class LogoutForm(FlaskForm):
    submit = SubmitField("Logout", id="btn-logout")


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=4, max=16)])
    repeat_password = PasswordField("Repeat new password", validators=[DataRequired(), Length(min=4, max=16)])
    submit = SubmitField("Change Password", id="btn-chpasswd")


class CookiesForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=16)])
    value = StringField("Value", validators=[DataRequired(), Length(min=4, max=50)])
    submit = SubmitField("Modify cookie", id="cookies")


class TodoForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter a task here"})
    save = SubmitField("Save")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter a name here"})
    surname = StringField("Surname", validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter a surname here"})
    login = StringField("Login", validators=[DataRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Enter an username here"})
    email = EmailField("Email", validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter an email here"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Enter a password here"})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Enter a  password here"})
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(min=5, max=255)], render_kw={"placeholder": "Enter an email here"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Enter a password here"})
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

