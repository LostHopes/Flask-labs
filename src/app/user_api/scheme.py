from flask_marshmallow import Schema
from flask_marshmallow.fields import fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    login = fields.Str(required=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    is_active = fields.Bool(dump_only=True)
    last_seen = fields.DateTime(dump_only=True)
    about = fields.Str()
    register_date = fields.DateTime(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

