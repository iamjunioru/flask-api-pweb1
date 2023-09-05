from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    JWT_SECRET_KEY = 'secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    