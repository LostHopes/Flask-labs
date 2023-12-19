from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class WritePostForm(FlaskForm):
    title = StringField("Post title", validators=[DataRequired(), Length(min=10, max=50)])
    text = TextAreaField("Post content", validators=[DataRequired(), Length(min=250, max=5000)], render_kw={"cols": "50", "rows": "15"})
    submit = SubmitField("Publish")


class EditPostForm(FlaskForm):
    title = StringField("Post title", validators=[DataRequired(), Length(min=10, max=50)])
    text = TextAreaField("Post content", validators=[DataRequired(), Length(min=250, max=5000)], render_kw={"cols": "50", "rows": "15"})
    submit = SubmitField("Edit")
