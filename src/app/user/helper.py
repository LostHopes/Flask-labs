from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import current_user
from PIL import Image

import os
import secrets

from app.user.models import Users
from app import login_manager, db, app


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)
    

class UsersHelper(Users):

    def __init__(self):
        self.path = lambda filename: os.path.join(app.root_path, "user",
         "static", "user", "images", "profile_pics", filename)

    def register(self, name: str, surname: str, login: str, email: str, password: str, confirm_password: str, register_date: str) -> None:
        
        password_hash = generate_password_hash(password)
        if check_password_hash(password_hash, confirm_password):
            user = Users(
                name=name,
                surname=surname,
                login=login,
                email=email,
                password=password_hash,
                register_date=register_date
            )
            db.session.add(user)
            db.session.commit()
    
    def profile(self):
        user_info = db.session.query(Users)
        return user_info

    def get_username(self, email: str) -> str:
        username = db.session.query(Users).filter_by(email=email).first()
        return username

    def get_all(self) -> list:
        users = db.session.query(Users).all()
        return users

    def login(self, email: str, password: str) -> bool|None:
        exist = db.session.query(
            Users.query.filter_by(email=email)\
                .exists()).scalar()
        if exist:
            info = Users.query.filter_by(email=email).first()
            validation = info.email == email and check_password_hash(info.password, password)
            return validation

    def change_password(self, new_password: str, repeat_password: str) -> bool:
        succeed = True
        
        validation = new_password == repeat_password

        if validation:
            password_hash = generate_password_hash(new_password)
            current_user.password = password_hash
            db.session.commit()
            return succeed

        return not succeed
        

    def save_picture(self, form_picture: str) -> str:
        random_hex = secrets.token_hex(8)
        _, file_extension = os.path.split(form_picture.filename)
        picture_filename = random_hex + file_extension
        picture_path = self.path(picture_filename)
        image = Image.open(form_picture)
        new_image = image.resize((300, 300))
        new_image.save(picture_path)
        return picture_filename
    
    
    def update(self, username: str, email: str, image: str, about: str) -> None:

        current_user.login = username
        current_user.email = email

        if image:
            self.delete_picture(current_user.image)
            current_user.image = self.save_picture(image)

        current_user.about = about


        self.commit()


    def delete_picture(self, filename: str) -> str:

        if filename == "default.jpg":
            return

        os.remove(self.path(filename))
        return filename


    @staticmethod
    def commit() -> None:
        db.session.commit()

    @staticmethod
    def rollback() -> None:
        db.session.rollback()

    
    def disable() -> bool:
        pass



