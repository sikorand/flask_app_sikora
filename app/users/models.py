from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
class User(UserMixin, db.Model):
    __tablename__='users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(120), unique=True,nullable=False)
    password = db.Column(db.String(60), nullable=False)

    @property
    def is_active(self):
        return True
    def __repr__(self):
        return f"User('(self.email)')"
    def get_id(self):
        return str(self.id)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)