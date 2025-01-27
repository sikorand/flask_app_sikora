from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name="config"):
    # Ініціалізація Flask додатка
    app = Flask(__name__)

    # Завантаження конфігурації
    if config_name == 'TestingConfig':
        app.config.from_object('config.TestingConfig')  # Задайте правильний шлях до класу
    else:
        app.config.from_object('config.Config')
    
    # Ініціалізація розширень
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Ініціалізація шляху для login_manager
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # Імпортуємо маршрути та моделі
    with app.app_context():
        from . import views
        from .posts.models import Post
        from .users.models import User
        from .posts import post_bp
        from .users import user_bp

        # Реєстрація блакитних принтів
        app.register_blueprint(post_bp)
        app.register_blueprint(user_bp)

    return app
