import requests

from constants import BASE_URL, USER_ENDPOINT, REGISTER_ENDPOINT, LOGIN_ENDPOINT, HEADERS

class TestAuthAPINegative:
    def test_try_register_user_with_non_valid_password(self, test_user_with_non_valid_password):
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"

        register_user_response = requests.post(register_url, json=test_user_with_non_valid_password, headers=HEADERS)

        assert register_user_response.status_code == 400, "Пользователь с невалидными данными создан"
        register_user_response_data = register_user_response.json()
        assert not register_user_response_data, "Пользователь с невалидными данными создан."

    def test_try_register_user_with_non_unique_email(self, test_user, test_user_2):
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"

        register_user_response = requests.post(register_url, json=test_user, headers=HEADERS)

        assert register_user_response.status_code == 201, "Ошибка регистрации пользователя."
        
        register_user_response_data = register_user_response.json()
        email = register_user_response_data['email']
        test_user_2['Email'] = email

        register_user_with_non_unique_email_response = requests.post(register_url, json=test_user_2, headers=HEADERS)

        assert register_user_with_non_unique_email_response.status_code == 409, 'Пользователь с не уникальным емейлом зарегистрирован.'
        register_user_with_non_unique_email_response_data = register_user_with_non_unique_email_response.status_code.json()
        assert not register_user_with_non_unique_email_response_data, "Пользователь с не уникальным емейлом зарегистрирован."

    def test_try_to_login_as_user_with_wrong_email(self, test_user):
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
        login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'

        register_user_response = requests.post(register_url, json=test_user, headers=HEADERS)

        assert register_user_response.status_code == 201, "Ошибка регистрации пользователя"

        test_user['password'] += '!'

        login_as_user_responce = requests.post(login_url, json=user_data_for_login(test_user), headers=HEADERS)

        assert login_as_user_responce.status_code == 401, 'Пользователь залогинился с не корректным паролем.'
        assert not login_as_user_responce.json(), 'Пользователь залогинился с не корректным паролем.'

    def test_try_to_create_user_with_non_unique_email_as_admin(self, admin_auth, test_user_created_by_admin, test_user_created_by_admin_2):
        create_user_url = f"{BASE_URL}{USER_ENDPOINT}"

        create_user_response = admin_auth.post(create_user_url, json=test_user_created_by_admin)

        assert create_user_response.status_code == 201, "Ошибка создания пользователя"

        first_user_email = create_user_response.json()['email']

        test_user_created_by_admin_2['email'] = first_user_email

        try_to_create_user_with_non_unique_email_response = admin_auth.post(create_user_url, json=test_user_created_by_admin_2)

        assert try_to_create_user_with_non_unique_email_response.status_code == 409, 'Пользователь с не уникальным емейлом создан.'
        assert not try_to_create_user_with_non_unique_email_response.json(), 'Пользователь с не уникальным емейлом создан.'

    def test_try_to_change_user_as_admin_with_wrong_role(self, admin_auth, test_user_created_by_admin, test_user_created_by_admin_change):
        create_user_url = f"{BASE_URL}{USER_ENDPOINT}"

        create_user_response = admin_auth.post(create_user_url, json=test_user_created_by_admin)

        assert create_user_response.status_code == 201, "Ошибка создания пользователя"
        created_user_id = create_user_response.json()['id']

        test_user_created_by_admin_change['roles'] = ['USEROK']

        change_user_response = admin_auth.patch(f'{create_user_url}/{created_user_id}', json=test_user_created_by_admin_change)

        assert change_user_response.status_code == 400, 'Получилось изменить роль пользователя на не корректную.'
        assert not change_user_response.json(), 'Получилось изменить роль пользователя на не корректную.'




