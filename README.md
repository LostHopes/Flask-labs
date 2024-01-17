# Самостійна робота №2, Варіант №12 - Фільми

## 1. Створення базових запитів

Вміст файлу views.py блюпринта **films**

```python
import flask_jwt_extended as jwt
from flask_restful import Resource, request

from datetime import datetime

from .scheme import film_scheme, films_scheme
from .models import Films
from app.user.models import Users
from app import db, api


class SingleFilmAPI(Resource):       

    def get(self, id):
        film = Films.query.get(id)

        if not film:
            return {"msg": "Film not found"}, 404

        return film_scheme.jsonify(film)

    @jwt.jwt_required()
    def delete(self, id):
        film = Films.query.get(id)

        if not film:
            return {"msg": "Film not found"}, 404

        indentity = jwt.get_jwt_identity()
        user = Users.query.filter_by(email=indentity).first()

        if film.user_id != user.id:
            return {"msg": "Unauthorized"}, 401

        db.session.delete(film)
        db.session.commit()
        return {"msg": "Film was deleted"}
        
    @jwt.jwt_required()
    def put(self, id):

        film = Films.query.get(id)

        if not film:
            return {"msg": "Film not found"}, 404

        data = request.get_json()

        indentity = jwt.get_jwt_identity()
        user = Users.query.filter_by(email=indentity).first()

        if film.user_id != user.id:
            return {"msg": "Unauthorized"}, 401

        film.name = data.get("name")
        film.date_out = datetime.strptime(data.get("date_out"), "%Y-%m-%d")
        film.time_added = datetime.now().replace(microsecond=0)
        film.genre = data.get("genre")
        film.user_id = user.id

        db.session.commit()

        return {"msg": "Film was successfully updated"}


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

        db.session.commit()

        return {"msg": "Film was successfully added"}


api.add_resource(SingleFilmAPI, "/api/films/<int:id>")
api.add_resource(GroupFilmAPI, "/api/films")
```

## 2. Безпека виконання операцій

Безпека операцій оновлення, додавання та видалення фільмів
здійснюється за допомогою валідного JWT токена
з допомогою декоратора *jwt_required* та метода *get_jwt_identity*.
Дивитися [Створення базових запитів](#1-створення-базових-запитів)
(У моєму випадку передача токена виконується через header)

## 3. Тестування за допомогою Postman

### 3.1 Запит POST на створення фільму

![image](/screenshots/films/films_1.png)

### 3.2 Запит GET на отримання одного фільму

![image](/screenshots/films/films_2.png)

### 3.3 Запит GET на отримання всіх фільмів

![image](/screenshots/films/films_3.png)

### 3.4 Запит PUT на оновлення фільму

![image](/screenshots/films/films_4.png)

### 3.5 Запит DELETE на видалення фільму

![image](/screenshots/films/films_5.png)


