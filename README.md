# Лабораторна №10 Рефакторинг за допомогою Blueprint та Factory method

## 1. Блюпринти

*user* blueprint

```python
from flask import Blueprint

user = Blueprint(
    "user",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import views, forms, models
```

*todo* blueprint

```python
from flask import Blueprint

todo = Blueprint(
    "todo",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import views, forms, models
```

*skills* blueprint

```python
from flask import Blueprint

skills = Blueprint(
    "skills",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import views, models
```

*cookies* blueprint

```python
from flask import Blueprint

cookies = Blueprint(
    "cookies",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import views, forms
```

*main* blueprint

```python
from flask import Blueprint

main = Blueprint(
    "main",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import views, errors
```

## 2. Ініціалізація блюпринтів, метод create_app та створення конфігурацій

### 2.1 Створення застосунка

```python
from flask import Flask
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
   
```

### 2.2 Створення конфігурацій

Вміст файлу *config.py*

```python
import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = b"secretkey123"


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or "sqlite:///" + os.path.join(basedir, "db", "users.sqlite")


class ProdConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or "sqlite:///" + os.path.join(basedir, "db", "users.sqlite")
```

Аргумент, шо задає конфігурацію [(див. Завдання 2.1)](#21-створення-застосунка)