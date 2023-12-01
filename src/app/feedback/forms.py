from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length
from wtforms import TextAreaField, SubmitField


class FeedbackForm(FlaskForm):
    text = TextAreaField("Text", validators=[DataRequired(), Length(min=40)])
    file = FileField("File", validators=[FileAllowed(["jpg", "png"], "Images only!")])
    submit = SubmitField("Publish")

