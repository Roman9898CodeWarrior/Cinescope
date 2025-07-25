import requests
from constants import BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
import pytest
from utils.data_generator import DataGenerator
from faker import Faker

faker = Faker()

@pytest.fixture(scope="session")
def test_user():
    random_email = DataGenerator.generate_valid_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_valid_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def test_user_2():
    random_email = DataGenerator.generate_valid_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_valid_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def test_user_with_non_valid_password():
    random_email = DataGenerator.generate_valid_random_email()
    random_name = DataGenerator.generate_random_name()
    random_non_valid_password = DataGenerator.generate_non_valid_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_non_valid_password,
        "passwordRepeat": random_non_valid_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def test_user_created_by_admin():
    random_email = DataGenerator.generate_valid_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_valid_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "verified": True,
        "banned": False
    }

@pytest.fixture(scope="session")
def test_user_created_by_admin_2():
    random_email = DataGenerator.generate_valid_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_valid_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "verified": True,
        "banned": False
    }

@pytest.fixture(scope="session")
def test_user_created_by_admin_change():
    random_email = DataGenerator.generate_valid_random_email()
    random_password = DataGenerator.generate_valid_random_password()

    return {
        "email": random_email,
        "password": random_password,
        "banned": True
    }


@pytest.fixture(scope="session")
def auth_session(test_user):
    # Регистрируем нового пользователя
    register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
    response = requests.post(register_url, json=test_user, headers=HEADERS)
    assert response.status_code == 201, "Ошибка регистрации пользователя"

    # Логинимся для получения токена
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = requests.post(login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации"

    # Получаем токен и создаём сессию
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture(scope='session')
def admin_auth():
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    response = requests.post(login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации"

    # Получаем токен и создаём сессию
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture(scope='session')
def user_data_for_login(test_user):
    return {'email': test_user['email'], 'password': test_user['password']}

@pytest.fixture(scope='session')
def admin_data_for_login():
    return {'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD}

@pytest.fixture(scope='session')
def payment_data():
    return {
        {
            "movieId": faker.random_choices(range(1,9), 10),
            "amount": faker.random_int(1, 10),
            "card": {
                "cardNumber": f"{faker.random_choices(range(0,9), 16)}",
                "cardHolder": f"{faker.first_name()} {faker.last_name()}",
                "expirationDate": f"{faker.random_int(1, 12)}/{faker.random_int(2025, 2035)}",
                "securityCode": faker.random_choices(range(0,9), 3)
            }
        }
    }