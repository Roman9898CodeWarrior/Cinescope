import requests

from constants import BASE_URL, USER_ENDPOINT, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT


class TestAuthAPIPositive:
    def test_register_user(self, test_user):
        # URL для регистрации
        register_url = f"{BASE_URL+REGISTER_ENDPOINT}"

        # Отправка запроса на регистрацию
        register_user_response = requests.post(url=register_url, json=test_user, headers=HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {register_user_response.status_code}")
        print(f"Response body: {register_user_response.text}")

        # Проверки
        assert register_user_response.status_code == 201, "Ошибка регистрации пользователя"
        register_user_response_data = register_user_response.json()
        assert register_user_response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in register_user_response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in register_user_response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in register_user_response_data["roles"], "Роль USER должна быть у пользователя"

    def test_login_as_user(self, test_user, user_data_for_login):
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
        login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'

        register_user_response = requests.post(register_url, json=test_user, headers=HEADERS)

        assert register_user_response.status_code == 201, "Ошибка регистрации пользователя"

        login_as_user_responce = requests.post(login_url, json=user_data_for_login(test_user), headers=HEADERS)

        assert login_as_user_responce.status_code == 200, 'Ошибка при попытке залогиниться.'

    def test_login_as_admin(self, admin_data_for_login):
        login_url = f'{BASE_URL}{LOGIN_ENDPOINT}'

        login_as_user_responce = requests.post(login_url, json=admin_data_for_login, headers=HEADERS)

        assert login_as_user_responce.status_code == 200, 'Ошибка при попытке залогиниться.'

    def test_create_user_as_admin(self, admin_auth, test_user_created_by_admin):
        create_user_url = f"{BASE_URL}{USER_ENDPOINT}"

        create_user_response = admin_auth.post(create_user_url, json=test_user_created_by_admin)

        assert create_user_response.status_code == 201, "Ошибка создания пользователя"
        create_user_response_data = create_user_response.json()
        created_user_id = create_user_response_data['id']

        assert create_user_response_data["email"] == test_user_created_by_admin["email"], "Email не совпадает"
        assert create_user_response_data['verified'] == test_user_created_by_admin['verified'], 'Значение того, верефицирован ли пользователь, не совпадает'
        assert "id" in create_user_response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in create_user_response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in create_user_response_data["roles"], "Роль USER должна быть у пользователя"

        get_user_response = admin_auth.get(f'{create_user_url}/{created_user_id}')

        assert get_user_response.status_code == 200, 'Пользователь не получен.'
        get_user_response_data = get_user_response.json()

        assert get_user_response_data["email"] == test_user_created_by_admin["email"], "Email не совпадает"
        assert get_user_response_data['verified'] == test_user_created_by_admin['verified'], 'Значение того, верефицирован ли пользователь, не совпадает'
        assert "id" in get_user_response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in get_user_response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in get_user_response_data["roles"], "Роль USER должна быть у пользователя"

    def test_change_user_as_admin(self, admin_auth, test_user_created_by_admin, test_user_created_by_admin_change):
        create_user_url = f"{BASE_URL}{USER_ENDPOINT}"

        create_user_response = admin_auth.post(create_user_url, json=test_user_created_by_admin)

        assert create_user_response.status_code == 201, "Ошибка создания пользователя"
        created_user_id = create_user_response.json()['id']

        change_user_response = admin_auth.patch(f'{create_user_url}/{created_user_id}', json=test_user_created_by_admin_change)

        assert change_user_response.status_code == 200, 'Ошибка изменения данных пользователя'
        change_user_response_data = change_user_response.json()

        assert change_user_response_data["email"] == test_user_created_by_admin_change["email"], "Email не совпадает"
        assert change_user_response_data["password"] == test_user_created_by_admin_change["password"], "Пароль не совпадает"
        assert change_user_response_data["banned"] == test_user_created_by_admin_change["banned"], "Забенен ли пользователь не совпадает"

        get_user_after_change_response = admin_auth.get(f'{create_user_url}/{created_user_id}')

        assert get_user_after_change_response.status_code == 200, 'Пользователь не получен.'
        get_user_after_change_response_data = get_user_after_change_response.json()
        assert get_user_after_change_response_data['id'] == test_user_created_by_admin['id'], 'id после изменения данных пользователя не совпадает с изначальным id'
        assert get_user_after_change_response_data["email"] == test_user_created_by_admin_change["email"], "Email не совпадает"
        assert get_user_after_change_response_data["password"] == test_user_created_by_admin_change[
            "password"], "Пароль не совпадает"
        assert get_user_after_change_response_data["banned"] == test_user_created_by_admin_change[
            "banned"], "Забенен ли пользователь не совпадает"
