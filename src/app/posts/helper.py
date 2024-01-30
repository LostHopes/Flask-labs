from flask import request
from PIL import Image
from flask_login import current_user

import os
import secrets

from app.posts.models import Posts
from app.user.models import Users
from app import db, app


class PostsHelper(Posts):

    def show(self, page, max_items):
        query = db.session.query(Posts, Users)\
            .join(Users).\
                order_by(Posts.created_at.desc())\
                    .paginate(page=page, per_page=max_items)
        return query

    def get(self, id):
        post = Posts.query.filter_by(id=id).first()
        return post
    
    def create(self, title, text, category, user_id):
        post = Posts(title=title, text=text, category=category, user_id=user_id)
        db.session.add(post)
        db.session.commit()

    def delete(self, id):
        post = Posts.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()

    def update(self, id, title, text, image, category):
        post = Posts.query.filter_by(id=id).first()
        post.title = title
        post.text = text
        post.category = category

        if image:
            post.image = self.save_picture(image)

        db.session.commit()

    @staticmethod
    def save_picture(file):
        random_hex = secrets.token_hex(8)
        _, file_extension = os.path.split(file.filename)
        full_filename = random_hex + file_extension
        path = os.path.join(app.root_path, "static", "images", "posts_thumbnails", full_filename)
        image = Image.open(file)
        new_image = image.resize((200, 200))
        new_image.save(path)
        return full_filename
