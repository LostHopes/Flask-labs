from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app import api, db
from app.user.models import Users
from .scheme import user_schema, users_schema


class UserAPI(Resource):
    def get(self, id):
        user = Users.query.filter_by(id=id).first_or_404("User not found")
        return user_schema.jsonify(user)

    def delete(self, id):
        user = Users.query.filter_by(id=id).first_or_404("User not found")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User was deleted"}

    def put(self, id):
        user = Users.query.filter_by(id=id).first_or_404("User not found")
        data = request.get_json()
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        password_hash = generate_password_hash(password)

        if check_password_hash(password_hash, confirm_password):
            user.login = data.get("login")
            user.email = data.get("email")
            user.password = password_hash
            user.last_seen = datetime.now().replace(second=0, microsecond=0)
            user.about = data.get("about")
            db.session.commit()
            return {"msg": "User was updated"}


class UsersGroupAPI(Resource):
    def get(self):
        users = Users.query.all()
        return users_schema.jsonify(users)

    def post(self):
        data = request.get_json()

        login = data.get("login")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        name = data.get("name")
        surname = data.get("surname")
        register_date = datetime.now().replace(microsecond=0, second=0)
        password_hash = generate_password_hash(password)

        if check_password_hash(password_hash, confirm_password):
            user = Users(
                login=login,
                email=email,
                password=password_hash,
                name=name,
                surname=surname,
                register_date=register_date
            )
            db.session.add(user)
            db.session.commit()
            return {"msg": "User was registered"}
        return {"msg": "User already exists"}, 409


api.add_resource(UserAPI, "/api/users/<int:id>")
api.add_resource(UsersGroupAPI, "/api/users")