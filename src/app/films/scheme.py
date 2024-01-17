from flask_marshmallow import Schema
from flask_marshmallow.fields import fields


class FilmSchema(Schema):
    name = fields.String()
    date_out = fields.Date()
    time_added = fields.DateTime()
    genre = fields.String()


film_scheme = FilmSchema()
films_scheme = FilmSchema(many=True)