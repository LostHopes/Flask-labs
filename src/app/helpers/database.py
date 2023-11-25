from flask_sqlalchemy import SQLAlchemy
from app.models import db, Todo, Users
from app import app
from flask_bcrypt import generate_password_hash, check_password_hash
from app.config import login_manager


with app.app_context():
    db.create_all(bind_key=None)

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(user_id)

class HandleUsers(Users):
    def register(self, name, surname, login, email, password, confirm_password):
        
        password_hash = generate_password_hash(password)
        if check_password_hash(password_hash, confirm_password):
            user = Users(
                name=name,
                surname=surname,
                login=login,
                email=email,
                password=password_hash
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
    
    def update(self, username, email):
        pass
    
    def delete():
        pass



class HandleTodos(Todo):
    def show(self, id):
        todos = db.session.query(Todo).where(Todo.user_id == id)
        return todos

    def remove(self, id: int | None):
        todo = Todo.query.filter_by(id=id).first()
        db.session.delete(todo)
        db.session.commit()

    def add(self, name: str, id: int):
        task = Todo(task=name, user_id=id)
        db.session.add(task)
        db.session.commit()

    def update(self, id: int):
        task = db.session.query(Todo).filter(Todo.id == id).first()
        task.status = "Completed"
        db.session.commit()

