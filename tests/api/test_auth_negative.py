import allure

from utils.request_utils import RequestUtils


class TestAuthAPINegative:
    @allure.feature("Функционал регистрации пользователя.")
    @allure.title('Тест на неуспешную попытку зарегистрировать пользователя с невалидным паролем.')
    def test_try_register_user_with_non_valid_password(self, api_manager,
                                                       fixture_data_with_non_valid_password_for_user_registration):
        register_user_response = api_manager.auth_api.register_user(fixture_data_with_non_valid_password_for_user_registration, 400)

        #with allure.step('Проверка того, что сообщение об ошибке в ответе корректное.'):
            #assert register_user_response['message'] == ['Пароль должен содержать хотя бы одну цифру'], "Текст ошибки не корректный."


    @allure.feature("Функционал регистрации пользователя.")
    @allure.title('Тест на неуспешную попытку зарегистрировать пользователя с неуникальной почтой.')
    def test_try_register_user_with_non_unique_email(self, api_manager, fixture_data_for_user_registration,
                                                     fixture_registered_user_data, super_admin):
        registered_user_email = fixture_registered_user_data['email']

        with allure.step('Данным для регистрации 2 пользователя присваивается почта уже зарегистрированного пользователя.'):
            test_user_2 = fixture_data_for_user_registration
            test_user_2['email'] = registered_user_email

        with allure.step('Осуществляется попытка зарегистрировать пользователя с неуникальной почтой.'):
            api_manager.auth_api.register_user(test_user_2, 409)

            super_admin.api.user_api.delete_user(fixture_registered_user_data['id'])

    @allure.feature("Функционал аутентификации пользователя.")
    @allure.title('Тест на неуспешную попытку пользователя залогиниться с некорректной почтой.')
    def test_try_to_login_as_user_with_wrong_email(self, api_manager, fixture_register_user_response, super_admin):
        registered_user_creds_data = RequestUtils.get_request_body(fixture_register_user_response)
        registered_user_creds_data['password'] += '!'

        try_to_authenticate_response = api_manager.auth_api.authenticate(registered_user_creds_data, 401)

        assert try_to_authenticate_response.json()['message'] == 'Неверный логин или пароль', "Текст ошибки не корректный."

        #super_admin.api.user_api.delete_user(fixture_register_user_response.json()['id'])

    @allure.feature("Функционал создания пользователя.")
    @allure.title('Тест на неуспешную попытку админа создать нового пользователя с неуникальной почтой.')
    def test_try_to_create_user_with_non_unique_email_as_admin(self, super_admin,
                                                               fixture_data_for_user_creation_by_admin):
        test_user_created_by_admin_data = fixture_data_for_user_creation_by_admin()

        create_user_response = super_admin.api.user_api.create_user_as_admin(test_user_created_by_admin_data)

        first_user_email = create_user_response['email']

        test_user_created_by_admin_2 = fixture_data_for_user_creation_by_admin()

        test_user_created_by_admin_2['email'] = first_user_email

        super_admin.api.user_api.create_user_as_admin(test_user_created_by_admin_2, 409)

        super_admin.api.user_api.delete_user(create_user_response['id'])

    @allure.feature("Функционал изменения данных пользователя.")
    @allure.title('Тест на неуспешную попытку админа изменить данные пользователя некорректными данными.')
    def test_try_to_change_user_as_admin_with_wrong_role(self, super_admin, fixture_data_for_user_creation_by_admin,
                                                         fixture_test_user_created_by_admin_changed_data):
        test_user_created_by_admin_data = fixture_data_for_user_creation_by_admin()

        create_user_response = super_admin.api.user_api.create_user_as_admin(test_user_created_by_admin_data)

        fixture_test_user_created_by_admin_changed_data['roles'] = ['USEROK']

        super_admin.api.user_api.change_user_data_as_admin(create_user_response, fixture_test_user_created_by_admin_changed_data, 400)

        super_admin.api.user_api.delete_user(create_user_response['id'])



