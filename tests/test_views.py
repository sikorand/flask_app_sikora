import unittest
from app import db, create_app
from flask_testing import TestCase
from bs4 import BeautifulSoup
from app.users.models import User  # Імпортуємо модель User

class UserViewsTests(TestCase):
    def create_app(self):
        app = create_app(config_name="TestingConfig")
        return app

    def setUp(self):
        # Створюємо таблиці в базі даних
        db.create_all()

    def tearDown(self):
        # Видаляємо таблиці після тестів
        db.session.remove()
        db.drop_all()

    # 1. Перевірка коректного завантаження сторінок реєстрації та входу
    def test_page_loading(self):
        # Перевіряємо, чи сторінка реєстрації завантажується
        response = self.client.get('/user/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

        # Перевіряємо, чи сторінка входу завантажується
        response = self.client.get('/user/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    # 2. Коректне збереження користувача у базі даних при реєстрації
    def test_user_registration(self):
        response = self.client.get('/user/register')
        soup = BeautifulSoup(response.data, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        self.assertIsNotNone(csrf_token)

        response = self.client.post('/user/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'confirm_password': 'password',
            'csrf_token': csrf_token
        })

        # Перевіряємо перенаправлення
        self.assertEqual(response.status_code, 302)
        self.assertIn('/user/login', response.headers['Location'])

        # Перевіряємо, чи користувач збережений у базі
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'testuser@example.com')

    # 3. Тестування входу і виходу користувача на сайті
    def test_user_login_and_logout(self):
        # Реєструємо користувача
        response = self.client.get('/user/register')
        soup = BeautifulSoup(response.data, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        self.client.post('/user/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'confirm_password': 'password',
            'csrf_token': csrf_token
        })

        # Логін користувача
        response = self.client.get('/user/login')
        soup = BeautifulSoup(response.data, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        response = self.client.post('/user/login', data={
            'email': 'testuser@example.com',
            'password': 'password',
            'csrf_token': csrf_token
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('/user/account', response.headers['Location'])  # Перевірка на успішний логін

        # Вихід користувача
        response = self.client.get('/user/logout')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/user/login', response.headers['Location'])  # Перевірка перенаправлення після виходу

if __name__ == '__main__':
    unittest.main()
