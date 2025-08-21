import requests
import pytest

from api.api_manager import ApiManager
from utils.data_generator import DataGenerator
from faker import Faker
from custom_requester.custom_requester import CustomRequester
from constants import AUTH_URL, PAYMENT_URL, HEADERS, USER_ENDPOINT, REGISTER_ENDPOINT, \
    LOGIN_ENDPOINT, CREATE_PAYMENT_ENDPOINT, ADMIN_LOGIN_DATA

faker = Faker()

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

'''
@pytest.fixture(scope="session")
def auth_requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=AUTH_URL)

@pytest.fixture(scope="session")
def payment_requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=PAYMENT_URL)
'''

@pytest.fixture
def fixture_test_user():
    def _test_user():
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

    return _test_user

@pytest.fixture
def fixture_register_user(api_manager, fixture_test_user):
    test_user_data = fixture_test_user()

    response = api_manager.auth_api.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user_data,
        expected_status=201
    )

    register_user_response_data = response.json()
    register_user_response_data['password'] = test_user_data['password']
    return register_user_response_data

@pytest.fixture
def fixture_login_as_user(api_manager, fixture_register_user):
    login_data = {
        "email":  fixture_register_user['email'],
        "password":  fixture_register_user['password']
    }

    login_as_user_response = api_manager.auth_api.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=login_data
    )

    login_as_user_response_data = login_as_user_response.json()
    login_as_user_response_data['password'] = login_data['password']
    access_token = login_as_user_response_data['accessToken']
    api_manager.auth_api._update_session_headers(api_manager.auth_api.session, Authorization=f"Bearer {access_token}")
    return login_as_user_response_data

@pytest.fixture
def fixture_height_order_login_as_user_function(api_manager, fixture_register_user):
    def _login_as_user():
        login_data = {
            "email":  fixture_register_user['email'],
            "password":  fixture_register_user['password']
        }

        login_as_user_response = api_manager.auth_api.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data
        )

        login_as_user_response_data = login_as_user_response.json()
        login_as_user_response_data['password'] = login_data['password']
        access_token = login_as_user_response_data['accessToken']
        api_manager.auth_api._update_session_headers(api_manager.auth_api.session, Authorization=f"Bearer {access_token}")
        return login_as_user_response_data

    return _login_as_user
'''
@pytest.fixture
def login_as_admin(api_manager):
    login_as_admin_response = api_manager.auth_api.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data= ADMIN_LOGIN_DATA
    )

    login_as_admin_response_data = login_as_admin_response.json()
    access_token = login_as_admin_response_data['accessToken']
    login_as_admin_response_data['password'] = ADMIN_LOGIN_DATA['password']
    api_manager.auth_api._update_session_headers(api_manager.auth_api.session, Authorization=f"Bearer {access_token}")
    return login_as_admin_response_data


@pytest.fixture()
def get_user(auth_requester, request):
    user_id = request.param
    yield user_id

    response = auth_requester.send_request(
        method="GET",
        endpoint=f'{USER_ENDPOINT}/{user_id}',
        expected_status=200
    )
    response_data = response.json()
    return response_data

@pytest.fixture()
def get_user_info(api_manager, register_user):
    api_manager.auth_api.login_as_admin()
    registered_user_id = register_user['id']

    get_user_response = api_manager.auth_api.send_request(
        method="GET",
        endpoint=f'{USER_ENDPOINT}/{registered_user_id}'
    )
    get_user_response_data = get_user_response.json()
    return get_user_response_data
'''

@pytest.fixture
def fixture_test_user_with_non_valid_password():
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

@pytest.fixture
def fixture_user_data_for_creation_by_admin():
    def _user_data_for_creation_by_admin():
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

    return _user_data_for_creation_by_admin

@pytest.fixture
def fixture_test_user_created_by_admin_changed_data():
    random_email = DataGenerator.generate_valid_random_email()

    return {
        "email": random_email,
        "banned": True
    }

'''
@pytest.fixture
def auth_session(test_user):
    def _auth_session():
        new_user_data = test_user()

        register_url = f"{AUTH_URL}{REGISTER_ENDPOINT}"
        register_user_response = requests.post(register_url, json=new_user_data, headers=HEADERS, verify=False)
        assert  register_user_response.status_code == 201, "Ошибка регистрации пользователя"
        user_id =  register_user_response.json()['id']

        login_url = f"{AUTH_URL}{LOGIN_ENDPOINT}"
        login_data = {
            "email": new_user_data["email"],
            "password": new_user_data["password"]
        }
        login_as_user_response = requests.post(login_url, json=login_data, headers=HEADERS, verify=False)
        assert login_as_user_response.status_code == 200, "Ошибка авторизации"

        login_as_user_response_data = login_as_user_response.json()
        access_token = login_as_user_response_data.get("accessToken")
        refresh_token = login_as_user_response_data.get("refreshToken")
        assert access_token is not None, "Токен доступа отсутствует в ответе."
        assert refresh_token is not None, "Токен обновления токена доступа отсутствует в ответе."

        session = requests.Session()
        session.headers.update(HEADERS)
        session.headers.update({"Authorization": f"Bearer {access_token}"})
        return session, user_id, access_token, refresh_token

    return _auth_session

@pytest.fixture
def admin_auth(auth_requester):
    login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }

    response = auth_requester.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=login_data
    )
    response_data = response.json()

    token = response_data["accessToken"]
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session
'''

@pytest.fixture
def fixture_payment_data():
    def _payment_data():
        movie_id = DataGenerator.get_movie_id()
        amount = DataGenerator.generate_random_amount()
        card_number = DataGenerator.generate_random_card_number()
        card_holder_name = DataGenerator.generate_random_name()
        expiration_date = DataGenerator.generate_random_expiration_date()
        security_code = DataGenerator.generate_random_security_code()

        return {
            "movieId":  movie_id,
            "amount": amount,
            "card": {
                "cardNumber": "4242424242424242",
                "cardHolder": card_holder_name,
                "expirationDate": "12/25",
                "securityCode": 123
            }
        }

    return _payment_data

@pytest.fixture
def fixture_non_valid_payment_data():
    def _non_valid_payment_data():
        movie_id = DataGenerator.get_movie_id()
        amount = DataGenerator.generate_random_amount()
        card_number = DataGenerator.generate_random_card_number()
        card_holder_name = DataGenerator.generate_random_name()
        expiration_date = DataGenerator.generate_random_expiration_date()
        security_code = DataGenerator.generate_random_security_code()

        return {
                 "movieId":  movie_id,
                "amount": amount,
                "card": {
                    "cardNumber": "4242424242424242",
                    "cardHolder": card_holder_name,
                    "expirationDate": "12/25",
                    "securityCode": 321
                }


        }

    return _non_valid_payment_data


@pytest.fixture
def fixture_create_payment(api_manager, fixture_payment_data, fixture_login_as_user):
    def _create_payment():
        create_payment_response = api_manager.payment_api.send_request(
            method="POST",
            endpoint=CREATE_PAYMENT_ENDPOINT,
            data=fixture_payment_data(),
            expected_status=201
        )

        return create_payment_response.json()

    return _create_payment







