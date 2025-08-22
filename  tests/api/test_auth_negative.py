import requests

from constants import AUTH_URL, USER_ENDPOINT, REGISTER_ENDPOINT, LOGIN_ENDPOINT, HEADERS

class TestAuthAPINegative:
    def test_try_register_user_with_non_valid_password(self, api_manager, fixture_test_user_with_non_valid_password):
        register_user_response = api_manager.auth_api.register_user(fixture_test_user_with_non_valid_password, 400)

        assert register_user_response['message'] == ['Пароль должен содержать хотя бы одну цифру'], "Текст ошибки не корректный."

    def test_try_register_user_with_non_unique_email(self, api_manager, fixture_test_user, fixture_register_user):
        registered_user_email = fixture_register_user['email']

        test_user_2 = fixture_test_user()
        test_user_2['email'] = registered_user_email

        api_manager.auth_api.register_user(test_user_2, 409)

    def test_try_to_login_as_user_with_wrong_email(self, api_manager, fixture_test_user):
        test_user_data = fixture_test_user()

        register_user_response = api_manager.auth_api.register_user(test_user_data)

        register_user_response['password'] += '!'

        try_to_login_response = api_manager.auth_api.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=register_user_response,
            expected_status=401
        )

        assert try_to_login_response.json()['message'] == 'Неверный логин или пароль', "Текст ошибки не корректный."

    def test_try_to_create_user_with_non_unique_email_as_admin(self, api_manager,
                                                               fixture_user_data_for_creation_by_admin):
        test_user_created_by_admin_data = fixture_user_data_for_creation_by_admin()

        create_user_response = api_manager.user_api.create_user_as_admin(api_manager, test_user_created_by_admin_data)

        first_user_email = create_user_response['email']

        test_user_created_by_admin_2 = fixture_user_data_for_creation_by_admin()

        test_user_created_by_admin_2['email'] = first_user_email

        api_manager.user_api.create_user_as_admin(api_manager, test_user_created_by_admin_2, 409)

    def test_try_to_change_user_as_admin_with_wrong_role(self, api_manager, fixture_user_data_for_creation_by_admin,
                                                         fixture_test_user_created_by_admin_changed_data):
        test_user_created_by_admin_data = fixture_user_data_for_creation_by_admin()

        create_user_response = api_manager.user_api.create_user_as_admin(api_manager, test_user_created_by_admin_data)

        fixture_test_user_created_by_admin_changed_data['roles'] = ['USEROK']

        api_manager.user_api.change_user_as_admin(api_manager, create_user_response, fixture_test_user_created_by_admin_changed_data, 400)


