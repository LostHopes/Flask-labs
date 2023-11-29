from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, EmailField, PasswordField,\
     SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed


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


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[Length(min=6, max=20)], render_kw={"placeholder": "Enter a new username here"})
    email = EmailField("Email", validators=[Length(min=4, max=20)], render_kw={"placeholder": "Enter a new email here"})
    about = TextAreaField("About Me")
    image = FileField("Select image to update", validators=[FileAllowed(["jpg", "png", "webp"], "Wrong file extension! Allowed formats: jpg, png, webp")])
    submit = SubmitField("Update")


class LogoutForm(FlaskForm):
    submit = SubmitField("Logout", id="btn-logout")


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=4, max=16)])
    repeat_password = PasswordField("Repeat new password", validators=[DataRequired(), Length(min=4, max=16)])
    submit = SubmitField("Change", id="btn-chpasswd")