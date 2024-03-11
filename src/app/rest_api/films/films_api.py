import flask_jwt_extended as jwt
from flask_restful import Resource, request

from datetime import datetime

from .scheme import film_scheme, films_scheme
from .models import Films
from app.user.models import Users
from app import db, api


class SingleFilmAPI(Resource):       

    def get(self, id):
        film = Films.query.filter_by(id=id).first_or_404("Film not found")
        return film_scheme.jsonify(film)

    @jwt.jwt_required()
    def delete(self, id):
        film = Films.query.filter_by(id=id).first_or_404("Film not found")

        indentity = jwt.get_jwt_identity()
        user = Users.query.filter_by(email=indentity).first()

        if film.user_id != user.id:
            return {"message": "Unauthorized"}, 401

        db.session.delete(film)
        db.session.commit()
        return {"message": "Film was deleted"}
        
    @jwt.jwt_required()
    def put(self, id):

        film = Films.query.filter_by(id=id).first_or_404("Film not found")

        data = request.get_json()

        indentity = jwt.get_jwt_identity()
        user = Users.query.filter_by(email=indentity).first()

        if film.user_id != user.id:
            return {"message": "Unauthorized"}, 401

        film.name = data.get("name")
        film.date_out = datetime.strptime(data.get("date_out"), "%Y-%m-%d")
        film.time_added = datetime.now().replace(microsecond=0)
        film.genre = data.get("genre")
        film.user_id = user.id

        db.session.commit()

        return {"message": "Film was successfully updated"}


class GroupFilmAPI(Resource):
    def get(self):
        film = Films.query.all()
        return films_scheme.jsonify(film)

    @jwt.jwt_required()
    def post(self):

        indentity = jwt.get_jwt_identity()
        user = Users.query.filter_by(email=indentity).first()

        data = request.get_json()

        film = Films()

        film.name = data.get("name")
        film.date_out = datetime.strptime(data.get("date_out"), "%Y-%m-%d")
        film.time_added = datetime.now().replace(microsecond=0)
        film.genre = data.get("genre")
        film.user_id = user.id
        
        db.session.add(film)
        db.session.commit()

        return {"message": "Film was successfully added"}


api.add_resource(SingleFilmAPI, "/api/films/<int:id>")
api.add_resource(GroupFilmAPI, "/api/films")





