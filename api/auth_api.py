from venv import logger

import pytest
from pydantic import ValidationError

from constants.constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, LOGOUT_ENDPOINT, REFRESH_TOKENS_ENDPOINT, AUTH_URL
from custom_requester.custom_requester import CustomRequester
from models.get_user_info_response_model import RegisterCreateGetOrDeleteUserResponse
from models.login_user_response_model import LogInResponse
from models.refresh_tokens_response_model import RefreshTokensResponse
from models.user_data_model import UserDataForLoggingIn, UserDataForRegistration


class AuthAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session, AUTH_URL)

    def authenticate(self, registered_user_data, expected_status=200):
        login_data = {}

        try:
            login_data = vars(
                UserDataForLoggingIn(
                    email=registered_user_data['email'],
                    password=registered_user_data['password']
                )
            )
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

        login_as_user_response = self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

        if expected_status != 200 and login_as_user_response.status_code != 200:
            return login_as_user_response
        else:
            try:
                login_as_user_response_validated = vars(LogInResponse(**login_as_user_response.json()))
                access_token = login_as_user_response_validated['accessToken']
                self._update_session_headers(Authorization=f"Bearer {access_token}")
                return login_as_user_response_validated
            except ValidationError as e:
                pytest.fail(f'Ошибка валидации: {e}')
                logger.info(f'Ошибка валидации: {e}')

    def height_order_authenticate_function(self, registered_user_data, expected_status=200):
        def _height_order_authenticate_function():
            login_data = {}

            try:
                login_data = vars(
                    UserDataForLoggingIn(
                        email=registered_user_data['email'],
                        password=registered_user_data['password']
                    )
                )
            except ValidationError as e:
                pytest.fail(f'Ошибка валидации: {e}')
                logger.info(f'Ошибка валидации: {e}')

            login_as_user_response = self.send_request(
                method="POST",
                endpoint=LOGIN_ENDPOINT,
                data=login_data,
                expected_status=expected_status
            )

            if expected_status != 200 and login_as_user_response.status_code != 200:
                return login_as_user_response
            else:
                try:
                    login_as_user_response_validated = vars(LogInResponse(**login_as_user_response.json()))
                    access_token = login_as_user_response_validated['accessToken']
                    self._update_session_headers(Authorization=f"Bearer {access_token}")
                    return login_as_user_response_validated
                except ValidationError as e:
                    pytest.fail(f'Ошибка валидации: {e}')
                    logger.info(f'Ошибка валидации: {e}')

        return _height_order_authenticate_function

    def register_user(self, test_user_data, expected_status=201):
        test_user_data_validated = {}

        try:
            test_user_data_validated = vars(UserDataForRegistration(**test_user_data))
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

        response = self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=test_user_data_validated,
            expected_status=expected_status
        )

        if expected_status != 200 and response.status_code != 200:
            return response.json()
        else:
            try:
                response_validated = vars(RegisterCreateGetOrDeleteUserResponse(**response.json()))
                return response_validated
            except ValidationError as e:
                pytest.fail(f'Ошибка валидации: {e}')
                logger.info(f'Ошибка валидации: {e}')



    def logout(self, expected_status=200):
        self.send_request(
            method="GET",
            endpoint=LOGOUT_ENDPOINT,
            expected_status=expected_status
        )

    def refresh_tokens(self, expected_status=200):
        refresh_tokens_response = self.send_request(
            method="GET",
            endpoint=REFRESH_TOKENS_ENDPOINT,
            expected_status=expected_status
        )

        try:
            refresh_tokens_response_validated = vars(RefreshTokensResponse(**refresh_tokens_response.json()))
            return refresh_tokens_response_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')


