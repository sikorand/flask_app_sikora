

class Config:
    SECRET_KEY = "secret-key-sdsfs"
    FLASK_DEBUG = 1 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    CSRF_ENABLED = True  # Включити CSRF для тестів
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = "secret-key-sdsfs"


