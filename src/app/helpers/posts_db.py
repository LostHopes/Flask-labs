from app.posts.models import Posts
from app.user.models import Users
from app import db


class PostsHelper(Posts):

    def show(self):
        query = db.session.query(Posts, Users).join(Users).all()
        return query
    
    def create(self, title, text, user_id):
        post = Posts(title=title, text=text, user_id=user_id)
        db.session.add(post)
        db.session.commit()

    def delete(self, id):
        post = Posts.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()

    def update(self, id, title, text):
        post = Posts.query.filter_by(id=id).first()
        post.title = title
        post.text = text
        db.session.commit()