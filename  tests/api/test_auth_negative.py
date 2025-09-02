from constants.constants import LOGIN_ENDPOINT
from models.user_data_model import UserDataForLoggingIn
from utils.request_utils import RequestUtils


class TestAuthAPINegative:
    def test_try_register_user_with_non_valid_password(self, api_manager,
                                                       fixture_user_data_for_registration_with_non_valid_password):
        register_user_response = api_manager.auth_api.register_user(fixture_user_data_for_registration_with_non_valid_password, 400)

        assert register_user_response['message'] == ['Пароль должен содержать хотя бы одну цифру'], "Текст ошибки не корректный."


    def test_try_register_user_with_non_unique_email(self, api_manager, fixture_user_data_for_registration_validated,
                                                     fixture_registered_user_data, super_admin):
        registered_user_email = fixture_registered_user_data['email']

        test_user_2 = fixture_user_data_for_registration_validated()
        test_user_2['email'] = registered_user_email

        api_manager.auth_api.register_user(test_user_2, 409)

        super_admin.api.user_api.delete_user(fixture_registered_user_data['id'])


    def test_try_to_login_as_user_with_wrong_email(self, api_manager, fixture_register_user_response, super_admin):
        registered_user_creds_data = RequestUtils.get_request_body(fixture_register_user_response)
        registered_user_creds_data['password'] += '!'

        try_to_authenticate_response = api_manager.auth_api.authenticate(registered_user_creds_data, 401)

        assert try_to_authenticate_response.json()['message'] == 'Неверный логин или пароль', "Текст ошибки не корректный."

        super_admin.api.user_api.delete_user(fixture_register_user_response.json()['id'])


    def test_try_to_create_user_with_non_unique_email_as_admin(self, super_admin,
                                                               fixture_user_data_for_creation_by_admin):
        test_user_created_by_admin_data = fixture_user_data_for_creation_by_admin()

        create_user_response = super_admin.api.user_api.create_user_as_admin(test_user_created_by_admin_data)

        first_user_email = create_user_response['email']

        test_user_created_by_admin_2 = fixture_user_data_for_creation_by_admin()

        test_user_created_by_admin_2['email'] = first_user_email

        super_admin.api.user_api.create_user_as_admin(test_user_created_by_admin_2, 409)

        super_admin.api.user_api.delete_user(create_user_response['id'])



    def test_try_to_change_user_as_admin_with_wrong_role(self, super_admin, fixture_user_data_for_creation_by_admin,
                                                         fixture_test_user_created_by_admin_changed_data):
        test_user_created_by_admin_data = fixture_user_data_for_creation_by_admin()

        create_user_response = super_admin.api.user_api.create_user_as_admin(test_user_created_by_admin_data)

        fixture_test_user_created_by_admin_changed_data['roles'] = ['USEROK']

        super_admin.api.user_api.change_user_as_admin(create_user_response, fixture_test_user_created_by_admin_changed_data, 400)



