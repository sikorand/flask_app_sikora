from . import post_bp
from flask import request, render_template, abort, flash, redirect, url_for
from app.posts.forms import PostForm
from app import db  # Імпортуємо об'єкт бази даних із вашої програми
from app.posts.models import Post  # Імпортуємо модель Post

@post_bp.route('/')
def get_posts():
    # Отримання всіх постів, відсортованих за датою публікації (спадання)
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template("posts.html", posts=posts)


@post_bp.route('/<int:id>')
def detail_post(id):
    # Знайти пост за ID
    post = Post.query.get_or_404(id)  # Отримуємо пост або 404, якщо не знайдено
    return render_template("detail_post.html", post=post)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        # Створюємо новий пост на основі даних форми
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            author="Admin"  # Заміна на поточного користувача, якщо використовується аутентифікація
        )
        db.session.add(new_post)
        db.session.commit()  # Зберігаємо зміни в базі даних
        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))
    return render_template('add_post.html', form=form)


@post_bp.route('/delete/<int:id>', methods=['GET','POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)  
    db.session.delete(post)  
    db.session.commit()  

    flash('Post has been deleted successfully!', 'success') 
    return redirect(url_for('posts.get_posts'))  

@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)  # Знайти пост по id
    form = PostForm(obj=post)  # Створити форму з даними поста

    if form.validate_on_submit():  # Якщо форма валідна і відправлена
        post.title = form.title.data
        post.content = form.content.data
        post.author = form.author.data  # Оновлення автора
        post.category = form.category.data  # Оновлення категорії
        post.posted = form.publish_date.data  # Оновлення дати публікації

        db.session.commit()  # Збереження змін у базі даних
        flash('Post updated successfully!', 'success')  # Повідомлення про успіх
        return redirect(url_for('posts.get_posts'))  # Перехід до списку постів

    return render_template('edit_post.html', form=form, post=post)  # Передача поста в шаблон


@post_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
