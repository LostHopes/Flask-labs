class Config:
    DEBUG = False
    SECRET_KEY = b"secretkey123"
    JWT_SECRET_KEY = b"secretkey123"
    JWT_TOKEN_LOCATION = ["headers", "query_string", "json"]
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.sqlite"


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    pass
