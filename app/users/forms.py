from flask_wtf import FlaskForm
from wtforms import TextAreaField,FileField,StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import  Optional,DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from .models import User
from app import bcrypt
from flask_login import current_user
from flask_wtf.file import FileAllowed
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

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About Me', validators=[Optional(), Length(max=500)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'webp'])])
    submit = SubmitField('Update')

    def __init__(self, original_email=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already registered. Please use a different one.')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

    def validate_current_password(self, form):
        # Перевірка, чи правильний поточний пароль
        if not check_password_hash(current_user, self.current_password.data):
            raise ValidationError('Current password is incorrect.')

    def save_new_password(self):
        # Збереження нового пароля
        new_hashed_password = bcrypt.generate_password_hash(self.new_password.data).decode('utf-8')
        current_user.password = new_hashed_password
        db.session.commit()


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password_hash(user, password):
    return bcrypt.check_password_hash(user.password, password)
