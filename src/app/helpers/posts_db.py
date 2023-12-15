from app.posts.models import Posts
from app import db


class PostsHelper(Posts):

    def show(self):
        query = Posts.query.all()
        return query
    
    def create(self, title, text, user_id):
        post = Posts(title=title, text=text, user_id=user_id)
        db.session.add(post)
        db.session.commit()

    def remove():
        pass

    def update():
        pass