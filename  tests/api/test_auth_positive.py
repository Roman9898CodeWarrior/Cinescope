from datetime import date

import requests

from api.api_manager import ApiManager
from constants import AUTH_URL, USER_ENDPOINT, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT, LOGOUT_ENDPOINT, \
    REFRESH_TOKENS_ENDPOINT


class TestAuthAPIPositive:
    def test_register_user(self, api_manager, fixture_test_user):
        test_user_data = fixture_test_user()

        register_user_response = api_manager.auth_api.register_user(test_user_data)

        assert "id" in register_user_response, "ID пользователя отсутствует в ответе."
        assert register_user_response['email'] == test_user_data['email'], "Email не совпадает."
        assert register_user_response["fullName"] == test_user_data["fullName"], "Имя и фамилия не совпадает."
        assert register_user_response["roles"] == test_user_data['roles'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert register_user_response['verified'] == True, 'Зарегистрированный пользователь не верефицирован.'
        assert register_user_response['banned'] == False, 'Зарегистрированный пользователь забанен.'
        assert date.today().strftime('%Y-%m-%d') in register_user_response['createdAt'], 'Дата регистрации пользователя не корректна.'


        get_user_response = api_manager.user_api.get_user_info(api_manager, register_user_response)

        assert get_user_response['id'] == register_user_response["id"], 'ID пользователя не корректное.'
        assert get_user_response["email"] == register_user_response["email"], "Email не совпадает."
        assert get_user_response["fullName"] == register_user_response["fullName"], "Имя и фамилия не совпадает."
        assert get_user_response["roles"] == register_user_response["roles"], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert get_user_response['verified'] == True, 'Зарегистрированный пользователь не верефицирован.'
        assert get_user_response['banned'] == False, 'Зарегистрированный пользователь забанен.'
        assert date.today().strftime('%Y-%m-%d') in get_user_response[
            'createdAt'], 'Дата регистрации пользователя не корректна.'


    def test_login_as_user(self, api_manager, fixture_register_user):
        login_as_user_response = api_manager.auth_api.login_as_user(fixture_register_user)

        assert login_as_user_response['user']['id'] == fixture_register_user['id'], 'id пользователя при аутентификации не корректный'
        assert login_as_user_response['user']["roles"] == fixture_register_user["roles"], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert 'accessToken' in login_as_user_response, 'В ответе отсутствует токен доступа.'
        assert 'refreshToken' in login_as_user_response, 'В ответе отсутствует токен обновления.'
        assert api_manager.session.headers['Authorization'] == f"Bearer {login_as_user_response['accessToken']}"
        assert api_manager.session.cookies['refresh_token'] == login_as_user_response['refreshToken']

    def test_logout_as_user(self, api_manager, fixture_login_as_user):
        #assert api_manager.session.headers['Authorization'] == f"Bearer {login_as_user_response['accessToken']}"
        assert api_manager.session.cookies['refresh_token'] == fixture_login_as_user['refreshToken']

        api_manager.auth_api.logout_as_user()
        #assert 'Authorization' not in api_manager.session.headers
        #assert api_manager.session.headers['Authorization'] == ''
        assert not api_manager.session.cookies


    def test_refresh_tokens(self, api_manager, fixture_login_as_user):
        initial_access_token = api_manager.session.headers['Authorization']
        initial_refresh_token = api_manager.session.cookies['refresh_token']

        refresh_tokens_response = api_manager.auth_api.refresh_tokens()

        #assert refresh_tokens_response['accessToken'] != initial_access_token
        assert refresh_tokens_response['refreshToken'] != initial_refresh_token

        #assert api_manager.session.headers['Authorization'] == f"Bearer {refresh_tokens_response['accessToken']}"
        assert api_manager.session.cookies['refresh_token'] == refresh_tokens_response['refreshToken']

    def test_login_as_admin(self, api_manager):
        login_as_admin_response = api_manager.auth_api.login_as_admin()

        assert 'id' in  login_as_admin_response['user'], 'В ответе отсутствует id админа.'
        assert 'ADMIN' in  login_as_admin_response['user']['roles'], 'У админа отсутствует роль ADMIN.'
        assert 'accessToken' in  login_as_admin_response, 'В ответе отсутствует токен доступа.'
        assert 'refreshToken' in login_as_admin_response, 'В ответе отсутствует токен обновления.'

        api_manager.session.headers['Authorization'] == f"Bearer {login_as_admin_response['accessToken']}", 'Токен доступа, который пришел в ответ на запрос авторизации, не установлен как токен доступа сессии.'
        assert api_manager.session.cookies['refresh_token'] == login_as_admin_response['refreshToken']

    def test_delete_user(self, api_manager, fixture_login_as_user):
        deleted_user_id = fixture_login_as_user['user']['id']

        delete_user_response = api_manager.user_api.delete_user(fixture_login_as_user)

        assert delete_user_response['id'] == deleted_user_id, 'id удаленного пользователя не совпадает с id пользователя, который должен был быть удален.'

        api_manager.auth_api.logout_as_user()

        api_manager.auth_api.login_as_admin()

        api_manager.user_api.send_request(
            method="GET",
            endpoint=f'{USER_ENDPOINT}/{deleted_user_id}',
            expected_status=404
        )


    def test_create_user_as_admin(self, api_manager, fixture_user_data_for_creation_by_admin):
        fixture_user_data_for_creation_by_admin = fixture_user_data_for_creation_by_admin()
        create_user_response = api_manager.user_api.create_user_as_admin(api_manager, fixture_user_data_for_creation_by_admin)

        assert 'id' in create_user_response, "ID пользователя отсутствует в ответе."
        assert create_user_response["email"] == fixture_user_data_for_creation_by_admin["email"], "Email не совпадает."
        assert create_user_response["fullName"] == fixture_user_data_for_creation_by_admin["fullName"], "Имя и фамилия не совпадает."
        assert create_user_response["roles"] == ['USER'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert create_user_response['verified'] == fixture_user_data_for_creation_by_admin["verified"], 'Зарегистрированный пользователь не верефицирован.'
        assert create_user_response['banned'] == fixture_user_data_for_creation_by_admin["banned"], 'Зарегистрированный пользователь забанен.'
        assert date.today().strftime('%Y-%m-%d') in create_user_response[
            'createdAt'], 'Дата регистрации пользователя не корректна.'

        get_created_user_response = api_manager.user_api.get_user_info(api_manager, create_user_response)

        assert get_created_user_response['id'] == create_user_response['id'], 'ID пользователя не корректное.'
        assert get_created_user_response["email"] == fixture_user_data_for_creation_by_admin["email"], "Email не совпадает."
        assert get_created_user_response["fullName"] == fixture_user_data_for_creation_by_admin["fullName"], "Имя и фамилия не совпадает."
        assert get_created_user_response["roles"] == ['USER'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert get_created_user_response['verified'] == fixture_user_data_for_creation_by_admin["verified"], 'Зарегистрированный пользователь не верефицирован.'
        assert get_created_user_response['banned'] == fixture_user_data_for_creation_by_admin["banned"], 'Зарегистрированный пользователь забанен.'
        assert date.today().strftime('%Y-%m-%d') in get_created_user_response[
            'createdAt'], 'Дата регистрации пользователя не корректна.'

    def test_change_user_as_admin(self, api_manager, fixture_user_data_for_creation_by_admin,
                                  fixture_test_user_created_by_admin_changed_data):
        fixture_user_data_for_creation_by_admin = fixture_user_data_for_creation_by_admin()

        create_user_response = api_manager.user_api.create_user_as_admin(api_manager, fixture_user_data_for_creation_by_admin)

        change_user_response = api_manager.user_api.change_user_as_admin(api_manager, create_user_response, fixture_test_user_created_by_admin_changed_data)

        assert change_user_response["email"] == fixture_test_user_created_by_admin_changed_data["email"], "Email не совпадает"
        assert change_user_response["banned"] == fixture_test_user_created_by_admin_changed_data["banned"], "Забенен ли пользователь не совпадает"
        #assert change_user_response['id'] == create_user_response['id'], 'ID пользователя не корректный.'
        assert change_user_response["fullName"] == create_user_response["fullName"], "Имя и фамилия не совпадает."
        assert change_user_response["roles"] == create_user_response['roles'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert change_user_response['verified'] == create_user_response['verified'], 'Зарегистрированный пользователь не верефицирован.'
        assert date.today().strftime('%Y-%m-%d') in change_user_response[
            'createdAt'], 'Дата регистрации пользователя отсутствует.'

        get_user_after_change_response = api_manager.user_api.get_user_info(api_manager, create_user_response)

        assert get_user_after_change_response["email"] == fixture_test_user_created_by_admin_changed_data["email"], "Email не совпадает"
        assert get_user_after_change_response["banned"] == fixture_test_user_created_by_admin_changed_data["banned"], "Забенен ли пользователь не совпадает"
        assert get_user_after_change_response['id'] == create_user_response['id'], 'ID пользователя не корректное.'
        assert get_user_after_change_response["fullName"] ==  create_user_response["fullName"], "Имя и фамилия не совпадает."
        assert get_user_after_change_response["roles"] == create_user_response['roles'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert get_user_after_change_response['verified'] == create_user_response['verified'], 'Зарегистрированный пользователь не верефицирован.'
        assert date.today().strftime('%Y-%m-%d') in get_user_after_change_response[
            'createdAt'], 'Дата регистрации пользователя отсутствует.'

    def test_get_all_users_filtered_by_role(self, api_manager):
        role = 'ADMIN'

        get_all_users_filtered_by_role_response = api_manager.user_api.get_all_users_filtered_by_role(api_manager, role)

        for user in get_all_users_filtered_by_role_response['users']:
            assert role in user['roles'], 'В отфильтрованном по роли "Админ" списке пользователей по крайней мере у одного пользователя нет роли администратора.'



