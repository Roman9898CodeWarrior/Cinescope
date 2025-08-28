from venv import logger

import requests
import pytest
from pydantic import ValidationError

from api.api_manager import ApiManager
from constants.roles import Roles
from entities.user import CommonUser
from entities.user import AdminUser
from models.login_user_response import LogInResponse
from models.register_user_response import RegisterOrCreateUserResponse
from models.user_data import UserDataForRegistration, UserDataForCreationByAdmin
from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator
from faker import Faker
from constants.constants import REGISTER_ENDPOINT, \
    LOGIN_ENDPOINT, CREATE_PAYMENT_ENDPOINT
from utils.request_utils import RequestUtils

faker = Faker()

@pytest.fixture(scope="session")
def basic_session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(basic_session):
    return ApiManager(basic_session)

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
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = AdminUser(
        SuperAdminCreds.EMAIL,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def common_user_registered(user_session, api_manager, fixture_user_for_registration):
    new_session = user_session()
    user_data_for_creation = fixture_user_for_registration()

    register_common_user_response = RegisterOrCreateUserResponse(**api_manager.auth_api.register_user(user_data_for_creation))

    common_user = CommonUser(
        user_data_for_creation['email'],
        user_data_for_creation['password'],
        user_data_for_creation['fullName'],
        register_common_user_response.id,
        register_common_user_response.roles,
        register_common_user_response.createdAt,
        register_common_user_response.verified,
        register_common_user_response.banned,
        new_session
    )

    logged_in_as_common_user_response = vars(LogInResponse(**common_user.api.auth_api.authenticate(user_data_for_creation)))

    common_user['accessToken'] = logged_in_as_common_user_response['accessToken'],
    common_user['refreshToken'] = logged_in_as_common_user_response['refreshToken']

    return common_user

@pytest.fixture
def common_user_created(user_session, super_admin, fixture_user_for_creation):
    new_session = user_session()
    user_data_for_creation = fixture_user_for_creation()

    created_common_user_response =  RegisterOrCreateUserResponse(**super_admin.api.user_api.create_user_as_admin(user_data_for_creation))

    common_user = CommonUser(
        user_data_for_creation['email'],
        user_data_for_creation['password'],
        user_data_for_creation['fullName'],
        created_common_user_response.id,
        created_common_user_response.roles,
        created_common_user_response.createdAt,
        user_data_for_creation['verified'],
        user_data_for_creation['banned'],
        new_session
    )

    logged_in_as_common_user_response = vars(LogInResponse(**common_user.api.auth_api.authenticate(user_data_for_creation)))

    common_user['accessToken'] = logged_in_as_common_user_response['accessToken'],
    common_user['refreshToken'] = logged_in_as_common_user_response['refreshToken']

    return common_user

@pytest.fixture
def fixture_user_for_registration(user_data_for_registration):
    def _test_user():
        try:
            user_data = UserDataForRegistration(**user_data_for_registration)
        except ValidationError as e:
            print(e)
            logger.info(f'Ошибка валидации: {e}')
        else:
            return vars(user_data)

    return _test_user

@pytest.fixture
def user_data_for_registration():
    random_email = DataGenerator.generate_valid_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_valid_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }

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
        "roles": [Roles.USER.value]
    }

@pytest.fixture
def fixture_user_for_creation(fixture_user_data_for_creation_by_admin):
    def _test_user():
        try:
            user_data = UserDataForCreationByAdmin(**fixture_user_data_for_creation_by_admin())
        except ValidationError as e:
            print(e)
            logger.info(f'Ошибка валидации: {e}')
        else:
            return vars(user_data)

    return _test_user

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

@pytest.fixture
def fixture_register_user_response(api_manager, fixture_user_for_registration):
    test_user_data = fixture_user_for_registration()

    return api_manager.auth_api.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user_data,
        expected_status=201
    )

@pytest.fixture
def fixture_register_user_data(api_manager, fixture_user_for_registration):
    test_user_data = fixture_user_for_registration()

    response = api_manager.auth_api.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user_data,
        expected_status=201
    )

    #register_user_response_data = response.json()
    #register_user_response_data['password'] = test_user_data['password']
    return response.json()

@pytest.fixture
def fixture_login_as_user(api_manager, fixture_register_user_response):
    registered_user_creds_data = RequestUtils.get_request_body(fixture_register_user_response)
    login_data = {
        "email":  registered_user_creds_data['email'],
        "password":  registered_user_creds_data['password']
    }

    login_as_user_response = api_manager.auth_api.send_request(
        method="POST",
        endpoint=LOGIN_ENDPOINT,
        data=login_data
    )

    login_as_user_response_data = login_as_user_response.json()
    #login_as_user_response_data['password'] = login_data['password']
    access_token = login_as_user_response_data['accessToken']
    api_manager.auth_api._update_session_headers(Authorization=f"Bearer {access_token}")
    return login_as_user_response_data

@pytest.fixture
def fixture_height_order_login_as_user_function(api_manager, fixture_register_user_response):
    def _login_as_user():
        registered_user_creds_data = RequestUtils.get_request_body(fixture_register_user_response)
        login_data = {
            "email": registered_user_creds_data['email'],
            "password": registered_user_creds_data['password']
        }

        login_as_user_response = api_manager.auth_api.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data
        )

        login_as_user_response_data = login_as_user_response.json()
        #login_as_user_response_data['password'] = login_data['password']
        access_token = login_as_user_response_data['accessToken']
        api_manager.auth_api._update_session_headers(Authorization=f"Bearer {access_token}")
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

'''
@pytest.fixture
def auth_session(test_user):
    def _auth_session():
        new_user_data = test_user()

        register_url = f"{AUTH_URL}{REGISTER_ENDPOINT}"
        register_user_response.py = requests.post(register_url, json=new_user_data, headers=HEADERS, verify=False)
        assert  register_user_response.py.status_code == 201, "Ошибка регистрации пользователя"
        user_id =  register_user_response.py.json()['id']

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







