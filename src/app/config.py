import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = b"secretkey123"
    JWT_SECRET_KEY = b"secretkey123"
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or "sqlite:///" + os.path.join(basedir, "db", "users.sqlite")


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProdConfig(Config):
    DEVELOPMENT = False
    DEBUG = False