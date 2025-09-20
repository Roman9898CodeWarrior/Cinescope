from venv import logger

import allure
import pytest
from pydantic import ValidationError

from API.api_tests_models.get_all_users_response_model import GetAllUsersDataResponseModel
from API.api_tests_models.get_user_info_response_model import RegisterCreateGetOrDeleteUserResponseModel, \
    ChangeUserDataResponseModel
from API.api_tests_models.login_user_response_model import AuthenticationResponseModel
from API.api_tests_models.refresh_tokens_response_model import RefreshTokenResponseModel
from API.api_tests_models.user_data_model import UserDataForAuthenticationModel, UserDataForRegistrationModel, \
    UserDataForCreationByAdminModel


class DataValidator:
    @staticmethod
    @allure.step('Валидация данных для аутентификации.')
    def validate_user_data_for_authentication(data_for_authentication):
        try:
            authentication_data_validated = vars(
                UserDataForAuthenticationModel(
                    email=data_for_authentication['email'],
                    password=data_for_authentication['password']
                )
            )
            return authentication_data_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    @staticmethod
    @allure.step('Валидация данных в ответе на запрос на аутентификацию.')
    def validate_authentication_response_data(authentication_response):
        try:
            authentication_response_data_validated = vars(AuthenticationResponseModel(**authentication_response.json()))
            return authentication_response_data_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    @staticmethod
    @allure.step('Валидация данных для регистрации.')
    def validate_user_data_for_registration(data_for_registration):
        try:
            registration_data_validated = vars(UserDataForRegistrationModel(**data_for_registration))
            return registration_data_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    @staticmethod
    @allure.step('Валидация данных в ответе на запрос на регистрацию/создание/удаление .')
    def validate_registration_creation_delete_or_getuserdata_response_data(response):
        try:
            response_data_validated = vars(
                RegisterCreateGetOrDeleteUserResponseModel(**response.json()))
            return response_data_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    @staticmethod
    @allure.step('Валидация данных в ответе на запрос на обновление токена.')
    def validate_refresh_token_response_data(refresh_token_response):
        try:
            refresh_token_response_data_validated = vars(
                RefreshTokenResponseModel(**refresh_token_response.json()))
            return refresh_token_response_data_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    @staticmethod
    @allure.step('Валидация данных для создания пользователя админом.')
    def validate_data_for_creation_user_by_admin(data_for_creation):
        try:
            creation_data_validated = vars(UserDataForCreationByAdminModel(**data_for_creation))
            return creation_data_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    @staticmethod
    @allure.step('Валидация данных в ответе на запрос на обновление данных пользователя.')
    def validate_change_user_data_response_data(change_user_data_response):
        try:
            change_user_data_response_data_validated = vars(
                ChangeUserDataResponseModel(**change_user_data_response.json()))
            return change_user_data_response_data_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    @staticmethod
    @allure.step('Валидация данных в ответе на запрос на получение данных всех пользователей.')
    def validate_get_all_users_data_response_data(get_all_users_data_response):
        try:
            get_all_users_data_response_data_validated = vars(
                GetAllUsersDataResponseModel(**get_all_users_data_response.json()))
            return get_all_users_data_response_data_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

