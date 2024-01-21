from flask import request

from app.posts.models import Posts
from app.user.models import Users
from app import db


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
    
    def create(self, title, text, category, image, user_id):
        post = Posts(title=title, text=text, category=category, image=image, user_id=user_id)
        db.session.add(post)
        db.session.commit()

    def delete(self, id):
        post = Posts.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()

    def update(self, id, title, text, category):
        post = Posts.query.filter_by(id=id).first()
        post.title = title
        post.text = text
        post.category = category
        db.session.commit()