from flask_restful import Resource
from flask import jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from datetime import datetime

from . import user_api
from app import api, db
from app.user.models import Users


class UserAPI(Resource):
    def get(self, id):

        user = Users.query.get(id)

        if not user:
            return {"msg": "User not found"}, 404

        return jsonify({f"{user.login}": {
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "is_active": user.is_active,
            "last_seen": user.last_seen,
            "about": user.about,
            "register_date": user.register_date
        }})

    def delete(self, id):
        user = Users.query.get(id)

        if not user:
            return {"msg": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"msg": "User was deleted"}

    def put(self, id):
        
        user = Users.query.get(id)

        if not user:
            return {"msg": "User not found"}, 404

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
            return {"msg": "User was updated"}


class UsersGroupAPI(Resource):
    def get(self):
        users = Users.query.all()
        
        user_list = [
        {
            "id": user.id,
            "login": user.login,
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "is_active": user.is_active,
            "last_seen": user.last_seen,
            "about": user.about,
            "register_date": user.register_date
        }
        for user in users
        ]
        return jsonify(users=user_list)

    def post(self):
        try:
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

        except IntegrityError:
            db.session.rollback()
            return {"msg": "User already exists"}

api.add_resource(UserAPI, "/api/users/<int:id>")
api.add_resource(UsersGroupAPI, "/api/users")