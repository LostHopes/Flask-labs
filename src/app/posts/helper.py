from flask import request
from PIL import Image

import os
import secrets

from app.posts.models import Posts, PostsTags
from app.user.models import Users
from app import db, app


class PostsHelper(Posts):

    def __init__(self):
        self.path = lambda filename: os.path.join(
            app.root_path, "posts", "static", "posts", "images", "posts_thumbnails", 
            filename)


    def show(self, page, max_items):
        query = db.session.query(Posts, Users)\
            .join(Users).\
                order_by(Posts.created_at.desc())\
                    .paginate(page=page, per_page=max_items)
        return query

    def get(self, id=None):

        if id is None:
            posts = Posts.query.all()
            return posts

        post = Posts.query.filter_by(id=id).first()
        return post
    
    def create(self, title, text, category, tags_str, image, user_id):

        post = Posts(title=title, text=text, category=category, user_id=user_id)

        if image:
            post.image = self.save_picture(image)

        db.session.add(post)
        db.session.commit()

        tags = [tag for tag in tags_str.split() if tag.startswith("#")]

        for tag in tags:
            posts_tags = PostsTags(name=tag, post_id=post.id)
            db.session.add(posts_tags)
        
        db.session.commit()

        

    def delete(self, id):
        post = Posts.query.filter_by(id=id).first()

        if not post:
            return

        self.delete_picture(post.image)

        db.session.delete(post)
        db.session.commit()

    def update(self, id, title, text, image, category, tags_str):
        post = Posts.query.filter_by(id=id).first()
        post.title = title
        post.text = text
        post.category = category

        if image:
            self.delete_picture(post.image)
            post.image = self.save_picture(image)

        tags = [tag for tag in tags_str.split() if tag.startswith("#")]

        for tag in tags:
            posts_tags = PostsTags(name=tag, post_id=post.id)

            exists = PostsTags.query.filter_by(post_id=id, name=tag).first()

            if not exists:

                db.session.add(posts_tags)
        
        db.session.commit()

    @staticmethod
    def get_famous_tags(amount=3):
        query  = db.session.query(PostsTags.name, db.func.count(PostsTags.name)).group_by(PostsTags.name).order_by(db.func.count(PostsTags.name).desc()).limit(amount).all()
        return query

    def save_picture(self, file):
        random_hex = secrets.token_hex(8)
        _, file_extension = os.path.split(file.filename)
        filename = random_hex + file_extension
        image = Image.open(file)
        new_image = image.resize((200, 200))
        new_image.save(self.path(filename))
        return filename

    def delete_picture(self, filename):

        if filename == "default.jpg":
            return

        os.remove(self.path(filename))
        return filename
