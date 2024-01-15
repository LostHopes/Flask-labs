from flask_restful import Resource

from . import user_api
from app import api


class UserAPI(Resource):
    def get(self, id):
        pass

    def delete(self, id):
        pass

    def put(self, id):
        pass


class UsersGroupAPI(Resource):
    def all(self):
        pass

    def create(self):
        pass


api.add_resource(UserAPI, "/api/users/<int:id>")
api.add_resource(UsersGroupAPI, "/api/users")