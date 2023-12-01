from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class CookiesForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=16)])
    value = StringField("Value", validators=[DataRequired(), Length(min=4, max=50)])
    submit = SubmitField("Modify cookie", id="cookies")