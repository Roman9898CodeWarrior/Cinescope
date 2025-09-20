from venv import logger

import allure
import pytest
import requests
from pydantic import ValidationError

from API.api_classes.api_manager import ApiManager
from API.api_tests_data.user_data import UserDataForApiTests
from API.api_tests_models.get_user_info_response_model import RegisterCreateGetOrDeleteUserResponseModel
from API.api_tests_models.user_data_model import UserDataForRegistrationModel
from API.entities.user import AdminUser
from constants.constants import REGISTER_ENDPOINT
from constants.roles import Roles
from resources.creds import SuperAdminCreds
from utils.request_utils import RequestUtils


@pytest.fixture
def user_session():
    user_sessions = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_sessions.append(user_session)
        return user_session

    yield _create_user_session

    for session in user_sessions:
        session.close_session()

@pytest.fixture
@allure.step('Аутентификация с учеткой админа.')
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
def fixture_data_for_user_registration():
    return UserDataForApiTests.get_user_data_for_registration()

@pytest.fixture
#@allure.step('Регистрация пользователя. В ответ получен response, а не тело ответа.')
def fixture_register_user_response(super_admin, fixture_data_for_user_registration):
    with allure.step('Регистрация пользователя. В ответ получен response, а не тело ответа.'):
        try:
            test_user_data_validated = vars(UserDataForRegistrationModel(**fixture_data_for_user_registration))
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

        response = super_admin.api.auth_api.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=test_user_data_validated,
            expected_status=201
        )

        try:
            vars(RegisterCreateGetOrDeleteUserResponseModel(**response.json()))
            yield response

            super_admin.api.user_api.delete_user(response.json()['id'])
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

@pytest.fixture
@allure.step('Получение из response.request ответа на запрос регистрации пользователя данных зарегистрированного пользователя (включая пароль, которого нет в самом ответе на регистрацию).')
def get_registered_user_data_from_response_request_of_registration_response(fixture_register_user_response):
    return RequestUtils.get_request_body(fixture_register_user_response)