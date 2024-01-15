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
    def register(self, name, surname, login, email, password, confirm_password, register_date):
        
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

    def get_username(self, email):
        username = db.session.query(Users).filter_by(email=email).first()
        return username

    def get_all(self):
        users = db.session.query(Users).all()
        return users

    def login(self, email, password):
        exist = db.session.query(
            Users.query.filter_by(email=email)\
                .exists()).scalar()
        if exist:
            info = Users.query.filter_by(email=email).first()
            validation = info.email == email and check_password_hash(info.password, password)
            return validation

    def change_password(self, new_password, repeat_password):
        succeed = False
        
        validation = new_password == repeat_password

        if validation:
            password_hash = generate_password_hash(new_password)
            current_user.password = password_hash
            db.session.commit()
            succeed = True
            return succeed

        return succeed
        
    @staticmethod
    def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        _, file_extension = os.path.split(form_picture.filename)
        picture_filename = random_hex + file_extension
        picture_path = os.path.join(app.root_path, "static", "images", "profile_pics", picture_filename)
        image = Image.open(form_picture)
        new_image = image.resize((300, 300))
        new_image.save(picture_path)
        return picture_filename
    
    
    def update(self, username, email, image, about):

        current_user.login = username
        current_user.email = email

        if image:
            current_user.image = self.save_picture(image)

        current_user.about = about


        self.commit()

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()

    
    def delete():
        pass



