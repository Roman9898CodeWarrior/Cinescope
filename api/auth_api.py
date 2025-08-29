from constants.constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, LOGOUT_ENDPOINT, REFRESH_TOKENS_ENDPOINT, AUTH_URL, ADMIN_LOGIN_DATA
from custom_requester.custom_requester import CustomRequester
from models.login_user_response import LogInResponse
from models.user_data import UserDataForLoggingIn


class AuthAPI(CustomRequester):
    def __init__(self, session):
        self.session = session
        super().__init__(session, AUTH_URL)

    def authenticate(self, registered_user_data, expected_status=200):
        login_data = vars(
            UserDataForLoggingIn(
                email=registered_user_data['email'],
                password=registered_user_data['password']
            )
        )

        login_as_user_response = self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

        if expected_status != 200 and login_as_user_response.status_code != 200:
            return login_as_user_response
        else:
            login_as_user_response_data = login_as_user_response.json()
            #login_as_user_response_data['password'] = login_data['password']
            access_token = login_as_user_response_data['accessToken']
            self._update_session_headers(Authorization=f"Bearer {access_token}")
            return login_as_user_response_data
    '''
    def log_in(self, registered_user_data, expected_status=200):
        login_data = vars(
            UserDataForLoggingIn(
                email=registered_user_data['email'],
                password=registered_user_data['password']
            )
        )

        login_as_user_response = self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

        if expected_status != 200 and login_as_user_response.status_code != 200:
            return login_as_user_response
        else:
            login_as_user_response_data = login_as_user_response.json()
            #login_as_user_response_data['password'] = login_data['password']
            access_token = login_as_user_response_data['accessToken']
            self._update_session_headers(Authorization=f"Bearer {access_token}")
            return login_as_user_response_data
    '''
    '''
    def login_user(self, login_data, expected_status=200):
        response = self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

        return response.json()
    '''

    def register_user(self, test_user_data, expected_status=201):
        response = self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=test_user_data,
            expected_status=expected_status
        )

        # register_user_response_data = response.json()
        #register_user_response_data['password'] = test_user_data['password']
        return response.json()


    def height_order_login_as_user_function(self, register_user, expected_status=200):
        def _login_as_user():
            login_data = {
                "email": register_user['email'],
                "password": register_user['password']
            }

            login_as_user_response = self.send_request(
                method="POST",
                endpoint=LOGIN_ENDPOINT,
                data=login_data,
                expected_status=expected_status
            )

            login_as_user_response_data = login_as_user_response.json()
            access_token = login_as_user_response_data['accessToken']
            login_as_user_response_data['password'] = login_data['password']
            self._update_session_headers(Authorization=f"Bearer {access_token}")
            return login_as_user_response_data

        return _login_as_user

    def login_as_admin(self, expected_status=200):
        login_as_admin_response = self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=ADMIN_LOGIN_DATA,
            expected_status=expected_status
        )

        login_as_admin_response_data = login_as_admin_response.json()
        login_as_admin_response_data['password'] = ADMIN_LOGIN_DATA['password']
        access_token = login_as_admin_response_data['accessToken']
        self._update_session_headers(Authorization=f"Bearer {access_token}")
        return login_as_admin_response_data

    def logout_as_user(self, expected_status=200):
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

        return refresh_tokens_response.json()

