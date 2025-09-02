import json
from venv import logger

import requests
import pytest
from pydantic import ValidationError

from api.api_manager import ApiManager
from constants.roles import Roles
from data.payment_data import PaymentData
from data.user_data import UserData
from entities.user import CommonUser
from entities.user import AdminUser
from models.login_user_response_model import LogInResponse
from models.payment_data_model import DataForPaymentCreation
from models.get_user_info_response_model import RegisterCreateGetOrDeleteUserResponse
from models.user_data_model import UserDataForRegistration, UserDataForCreationByAdmin, UserDataForLoggingIn
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
def common_user_registered(user_session, api_manager, fixture_user_data_for_registration_validated):
    new_session = user_session()
    user_data_for_creation_registration = fixture_user_data_for_registration_validated()

    register_common_user_response_validated = {}

    try:
        register_common_user_response_validated = RegisterCreateGetOrDeleteUserResponse(**api_manager.auth_api.register_user(user_data_for_creation_registration))
    except ValidationError as e:
        print(e)
        logger.info(f'Ошибка валидации: {e}')

    common_user = CommonUser(
        user_data_for_creation_registration['email'],
        user_data_for_creation_registration['password'],
        user_data_for_creation_registration['fullName'],
        register_common_user_response_validated.id,
        register_common_user_response_validated.roles,
        register_common_user_response_validated.createdAt,
        register_common_user_response_validated.verified,
        register_common_user_response_validated.banned,
        new_session
    )

    logged_in_as_common_user_response = common_user.api.auth_api.authenticate(user_data_for_creation_registration)

    common_user['accessToken'] = logged_in_as_common_user_response['accessToken'],
    common_user['refreshToken'] = logged_in_as_common_user_response['refreshToken']

    return common_user

@pytest.fixture
def common_user_created(user_session, super_admin, fixture_user_for_creation):
    new_session = user_session()
    user_data_for_creation = fixture_user_for_creation()

    created_common_user_response_validated = {}

    try:
        created_common_user_response_validated = RegisterCreateGetOrDeleteUserResponse(**super_admin.api.user_api.create_user_as_admin(user_data_for_creation))
    except ValidationError as e:
        pytest.fail(f'Ошибка валидации: {e}')
        logger.info(f'Ошибка валидации: {e}')

    common_user = CommonUser(
        user_data_for_creation['email'],
        user_data_for_creation['password'],
        user_data_for_creation['fullName'],
        created_common_user_response_validated.id,
        created_common_user_response_validated.roles,
        created_common_user_response_validated.createdAt,
        user_data_for_creation['verified'],
        user_data_for_creation['banned'],
        new_session
    )

    logged_in_as_common_user_response = common_user.api.auth_api.authenticate(user_data_for_creation)

    common_user['accessToken'] = logged_in_as_common_user_response['accessToken'],
    common_user['refreshToken'] = logged_in_as_common_user_response['refreshToken']

    return common_user

@pytest.fixture
def fixture_user_data_for_registration_validated(fixture_user_data_for_registration):
    def _user_data_for_registration_validated():
        try:
            user_data_for_registration_validated = vars(UserDataForRegistration(**fixture_user_data_for_registration))
            return user_data_for_registration_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    return _user_data_for_registration_validated

@pytest.fixture
def fixture_user_data_for_registration():
    return UserData.get_user_data_for_registration()

@pytest.fixture
def fixture_user_data_for_registration_with_non_valid_password():
    return UserData.get_non_valid_user_data_for_registration()

@pytest.fixture
def fixture_user_for_creation(fixture_user_data_for_creation_by_admin):
    def _test_user():
        try:
            user_data_for_creation_validated = vars(UserDataForCreationByAdmin(**fixture_user_data_for_creation_by_admin()))
            return user_data_for_creation_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    return _test_user

@pytest.fixture
def fixture_user_data_for_creation_by_admin():
    def _user_data_for_creation_by_admin():
        return UserData.get_user_data_for_creation_by_admin()

    return _user_data_for_creation_by_admin

@pytest.fixture
def fixture_test_user_created_by_admin_changed_data():
    return UserData.get_user_data_for_change_by_admin()

@pytest.fixture
def fixture_register_user_response(api_manager, fixture_user_data_for_registration_validated):
    test_user_data = fixture_user_data_for_registration_validated()
    test_user_data_validated = {}

    try:
        test_user_data_validated = vars(UserDataForRegistration(**test_user_data))
    except ValidationError as e:
        pytest.fail(f'Ошибка валидации: {e}')
        logger.info(f'Ошибка валидации: {e}')

    response = api_manager.auth_api.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user_data_validated,
        expected_status=201
    )

    try:
        vars(RegisterCreateGetOrDeleteUserResponse(**response.json()))
        return response
    except ValidationError as e:
        pytest.fail(f'Ошибка валидации: {e}')
        logger.info(f'Ошибка валидации: {e}')

@pytest.fixture
def fixture_registered_user_data(api_manager, fixture_user_data_for_registration_validated):
    test_user_data = fixture_user_data_for_registration_validated()

    return api_manager.auth_api.register_user(test_user_data)

@pytest.fixture
def fixture_authenticate(api_manager, fixture_register_user_response):
    registered_user_creds_data = RequestUtils.get_request_body(fixture_register_user_response)

    return api_manager.auth_api.authenticate(registered_user_creds_data)

@pytest.fixture
def fixture_height_order_authenticate_function(api_manager, fixture_register_user_response):
    def _height_order_authenticate_function():
        registered_user_creds_data = RequestUtils.get_request_body(fixture_register_user_response)

        return api_manager.auth_api.authenticate(registered_user_creds_data)

    return _height_order_authenticate_function

@pytest.fixture
def fixture_payment(fixture_valid_payment_data):
    def _fixture_payment():
        try:
            payment_data_validated = vars(DataForPaymentCreation(**fixture_valid_payment_data()))
            return payment_data_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    return _fixture_payment

@pytest.fixture
def fixture_valid_payment_data():
    def _valid_payment_data():
        return PaymentData.get_valid_payment_data()

    return _valid_payment_data

@pytest.fixture
def fixture_non_valid_payment_data():
    def _non_valid_payment_data():
        return PaymentData.get_non_valid_payment_data()

    return _non_valid_payment_data

@pytest.fixture
def fixture_create_payment(fixture_payment, common_user_registered):
    def _create_payment():
        create_payment_response = common_user_registered.api.payment_api.create_payment(
            data=fixture_payment()
        )

        return create_payment_response

    return _create_payment







