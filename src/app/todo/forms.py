from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class TodoForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter a task here"})
    save = SubmitField("Save")