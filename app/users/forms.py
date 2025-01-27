from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from .models import User
from app import bcrypt

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16), 
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 
                                                          message="Username must start with a letter and contain only letters, numbers, dots, or underscores.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already taken.")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password_hash(user, password):
    return bcrypt.check_password_hash(user.password, password)
