credentials = {
    "user1": "password123",
    "user2": "mySecurePassword",
    "admin": "adminPass",
    "guest": "guest1234",
    "testUser": "testPass456"
}
def authenticate_user(username, password):
    """Перевірка автентифікації користувача."""
    return credentials.get(username) == password