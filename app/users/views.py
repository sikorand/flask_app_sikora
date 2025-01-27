from . import user_bp
from flask import request, redirect, url_for, render_template, session, flash, make_response
from datetime import timedelta, datetime
from .forms import hash_password, check_password_hash
from .forms import RegistrationForm,LoginForm, UpdateAccountForm, ChangePasswordForm
from .models import User
from app import db, bcrypt
from flask_login import login_user,logout_user,current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from flask_login import user_logged_in

@user_bp.route('/')
def main():
    return render_template("base.html")



@user_bp.route("/hi/<string:name>")   
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", 
                           name=name, age=age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@user_bp.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@user_bp.route('/set_color/<color>')
def set_color(color):
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('color_scheme', color)
    return response



@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if not form.validate_on_submit():
        print('Form errors:', form.errors)
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Генерація хешу пароля
        hashed_password = hash_password(password)

        # Створення нового користувача з хешованим паролем
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', category='success')

        # Перевірте, чи дійсно виконується перенаправлення
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)

@user_bp.route('/users', methods=['GET'])
@login_required
def users_list():
    users = User.query.all()  # Отримуємо всіх користувачів з БД
    if not users:
        flash('No users found.', category='info')  # Повідомлення, якщо користувачів немає
        return render_template('users_list.html', users=None, title='Users')

    return render_template('users_list.html', users=users, title='Users List')


@user_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(original_email=current_user.email)
    password_form = ChangePasswordForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    # Зміна пароля
    if password_form.validate_on_submit():
        current_password = password_form.current_password.data
        new_password = password_form.new_password.data

    # Перевірка, чи введено поточний пароль
        if current_password and check_password_hash(current_user.password, current_password):
            # Якщо пароль вірний, хешуємо новий пароль
            current_user.password = hash_password(new_password)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('users.account'))
        elif not current_password:
            flash('Please enter your current password.', 'danger')
        else:
            flash('Current password is incorrect.', 'danger')




    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about_me.data = current_user.about_me

    return render_template('account.html', form=form, password_form=password_form, user=current_user)
from flask_login import user_logged_in

@user_logged_in.connect
def update_last_seen(sender, **kwargs):
    user = kwargs.get('user')
    if user:
        user.update_last_seen()  # Оновлюємо дату останнього входу
        db.session.commit()


from PIL import Image
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (150, 150)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Login successful!', 'success')
            session['username'] = user.username
            login_user(user)
            return redirect(url_for('users.account'))
        else:
            flash('Invalid email or password.', 'danger')

    # Передаємо об'єкт форми в шаблон
    return render_template('login.html', form=form)

from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




















@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if "username" in session:
        if request.method == 'POST':
            # Додавання кукі
            if 'key-cookie' in request.form and 'value-cookie' in request.form:
                key = request.form['key-cookie']
                value = request.form['value-cookie']
                expires = int(request.form['expires'])
                response = make_response(redirect(url_for('users.profile')))
                response.set_cookie(key, value, max_age=expires)
                flash('Кука додана успішно!', 'success')
                return response

            # Видалення кукі за ключем
            if 'delete-cookie' in request.form:
                key = request.form['delete-cookie']
                response = make_response(redirect(url_for('users.profile')))
                response.set_cookie(key, '', expires=0)
                flash('Кука видалена успішно!', 'success')
                return response

            # Видалення всіх кукі
            if 'delete-all-cookies' in request.form:
                response = make_response(redirect(url_for('users.profile')))
                for cookie in request.cookies:
                    response.set_cookie(cookie, '', expires=0)
                flash('Всі кукі видалені успішно!', 'success')
                return response
        username_value = session["username"]
        cookies = request.cookies
        return render_template("profile.html", username=username_value, cookies=cookies)
    flash("Invalid: Session.", "danger")
    return redirect(url_for("users.login"))



@user_bp.route('/logout')
def logout():
    logout_user()  # Завершення сесії Flask-Login
    flash('You have successfully logged out.', category='success')
    return redirect(url_for('users.login'))

@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60), path='/')
    # Якщо ви хочете просто видалити куку color, ви можете зробити це
    response.set_cookie('color', '', expires=0, path='/')  # видаляємо куку color
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
        return f'Користувач: {username}'
    return 'Кука не знайдена'

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0, path='/')  # видаляємо куку username
    return response