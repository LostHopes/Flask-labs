from flask import Flask, current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from .config import DevConfig


app = Flask(__name__)

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message = "You should login before accessing this page"
login_manager.login_message_category = "info"

def create_app(config_class=DevConfig):
    
    from .main import main
    app.register_blueprint(main)
    
    from .user import user
    app.register_blueprint(user)

    from .feedback import feedback
    app.register_blueprint(feedback, url_prefix="/feedback")

    from .todo import todo
    app.register_blueprint(todo, url_prefix="/todo")

    from .cookies import cookies
    app.register_blueprint(cookies, url_prefix="/cookies")

    from .skills import skills
    app.register_blueprint(skills, url_prefix="/skills")
    
    with app.app_context():
        app.config.from_object(config_class)
        db.init_app(app)
        migrate.init_app(app, db)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        db.create_all(bind_key=None)
        
    return app
   