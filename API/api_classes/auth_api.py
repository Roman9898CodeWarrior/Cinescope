import allure

from constants.constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, LOGOUT_ENDPOINT, REFRESH_TOKENS_ENDPOINT, AUTH_URL
from API.custom_requester import CustomRequester
from utils.data_validator import DataValidator


class AuthAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session, AUTH_URL)


    @allure.step("Аутентификация.")
    def authenticate(self, registered_user_data, expected_status=200):
        user_data_for_authentication_validated = DataValidator.validate_user_data_for_authentication(registered_user_data)

        login_as_user_response = self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=user_data_for_authentication_validated,
            expected_status=expected_status
        )

        if expected_status != 200 and login_as_user_response.status_code != 200:
            return login_as_user_response
        else:
            login_as_user_response_validated = DataValidator.validate_authentication_response_data(login_as_user_response)
            access_token = login_as_user_response_validated['accessToken']
            self._update_session_headers(Authorization=f"Bearer {access_token}")
            return login_as_user_response_validated


    def height_order_authenticate_function(self, registered_user_data, expected_status=201):
        def _height_order_authenticate_function():
            user_data_for_authentication_validated = DataValidator.validate_user_data_for_authentication(
                registered_user_data)

            login_as_user_response = self.send_request(
                method="POST",
                endpoint=LOGIN_ENDPOINT,
                data=user_data_for_authentication_validated,
                expected_status=expected_status
            )

            if expected_status != 200 and login_as_user_response.status_code != 200:
                return login_as_user_response
            else:
                login_as_user_response_validated = DataValidator.validate_authentication_response_data(
                    login_as_user_response)
                access_token = login_as_user_response_validated['accessToken']
                self._update_session_headers(Authorization=f"Bearer {access_token}")
                return login_as_user_response_validated

        return _height_order_authenticate_function


    @allure.step("Регистрация пользователя.")
    def register_user(self, data_for_registration, expected_status=201):
        data_for_registration_validated = DataValidator.validate_user_data_for_registration(data_for_registration)

        register_user_response = self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=data_for_registration_validated,
            expected_status=expected_status
        )

        if expected_status != 201 and register_user_response.status_code != 201:
            return register_user_response.json()
        else:
            registration_user_response_data_validated = DataValidator.validate_registration_creation_delete_or_getuserdata_response_data(register_user_response)
            return registration_user_response_data_validated


    @allure.step("Логаут.")
    def logout(self, expected_status=200):
        self.send_request(
            method="GET",
            endpoint=LOGOUT_ENDPOINT,
            expected_status=expected_status
        )

    @allure.step("Обновление токена.")
    def refresh_tokens(self, expected_status=200):
        refresh_token_response = self.send_request(
            method="GET",
            endpoint=REFRESH_TOKENS_ENDPOINT,
            expected_status=expected_status
        )

        refresh_tokens_response_data_validated = DataValidator.validate_refresh_token_response_data(refresh_token_response)
        return refresh_tokens_response_data_validated



