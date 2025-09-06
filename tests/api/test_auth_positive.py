import datetime
from datetime import date

import allure
import pytest

from constants.constants import USER_ENDPOINT
from constants.roles import Roles
from data.user_data import UserData
from models.user_data_model import UserDBModel
from utils.request_utils import RequestUtils


class TestAuthAPIPositive:
    @pytest.mark.smoke
    @allure.tag("smoke", "regression")
    @allure.label("owner", "Roman")
    @allure.feature("Функционал работы с пользователем.")
    @allure.title('Тест на успешную регистрацию пользователя.')
    def test_register_user(self, api_manager, fixture_user_data_for_registration_validated, super_admin, db_session):
        test_user_data = fixture_user_data_for_registration_validated()

        register_user_response = api_manager.auth_api.register_user(test_user_data)

        assert "id" in register_user_response, "ID пользователя отсутствует в ответе."
        assert register_user_response['email'] == test_user_data['email'], "Email не совпадает."
        assert register_user_response["fullName"] == test_user_data["fullName"], "Имя и фамилия не совпадает."
        assert register_user_response["roles"] == test_user_data['roles'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert register_user_response['verified'] == True, 'Зарегистрированный пользователь не верефицирован.'
        assert register_user_response['banned'] == False, 'Зарегистрированный пользователь забанен.'
        assert date.today().strftime('%Y-%m-%d') in register_user_response['createdAt'], 'Дата регистрации пользователя не корректна.'

        get_user_response = super_admin.api.user_api.get_user_info(register_user_response)

        assert get_user_response['id'] == register_user_response["id"], 'ID пользователя не корректное.'
        assert get_user_response["email"] == register_user_response["email"], "Email не совпадает."
        assert get_user_response["fullName"] == register_user_response["fullName"], "Имя и фамилия не совпадает."
        assert get_user_response["roles"] == register_user_response["roles"], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert get_user_response['verified'] == True, 'Зарегистрированный пользователь не верефицирован.'
        assert get_user_response['banned'] == False, 'Зарегистрированный пользователь забанен.'
        assert date.today().strftime('%Y-%m-%d') in get_user_response[
            'createdAt'], 'Дата регистрации пользователя не корректна.'

        '''
        users_from_db = db_session.query(UserDBModel).filter(UserDBModel.id == register_user_response.id)

        assert users_from_db.count() == 1, "обьект не попал в базу данных"
        
        user_from_db = users_from_db.first()
        '''

        super_admin.api.user_api.delete_user(register_user_response['id'])

    @pytest.mark.smoke
    @allure.tag("smoke", "regression")
    @allure.label("owner", "Roman")
    @allure.feature("Функционал аутентификации пользователя.")
    @allure.title('Тест на успешную аутентификацию пользователя.')
    def test_login_as_user(self, api_manager, fixture_register_user_response, super_admin):
        registered_user_creds_data = RequestUtils.get_request_body(fixture_register_user_response)
        login_as_user_response = api_manager.auth_api.authenticate(registered_user_creds_data)

        register_user_response_data = fixture_register_user_response.json()

        assert login_as_user_response['user']['id'] == register_user_response_data['id'], 'id пользователя при аутентификации не корректный'
        assert login_as_user_response['user']["roles"] == register_user_response_data["roles"], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert 'accessToken' in login_as_user_response, 'В ответе отсутствует токен доступа.'
        assert 'refreshToken' in login_as_user_response, 'В ответе отсутствует токен обновления.'
        assert api_manager.session.headers['Authorization'] == f"Bearer {login_as_user_response['accessToken']}"
        assert api_manager.session.cookies['refresh_token'] == login_as_user_response['refreshToken']

        #super_admin.api.user_api.delete_user(register_user_response_data['id'])


    '''
    def test_logout_as_user(self, api_manager, fixture_login_as_user):
        # ssert api_manager.session.headers['Authorization'] == f"Bearer {login_as_user_response['accessToken']}"
        assert api_manager.session.cookies['refresh_token'] == fixture_login_as_user['refreshToken']

        api_manager.auth_api.logout_as_user()
        # assert 'Authorization' not in api_manager.session.headers
        # assert api_manager.session.headers['Authorization'] == ''
        assert not api_manager.session.cookies

    '''

    @pytest.mark.smoke
    @allure.tag("smoke", "regression")
    @allure.label("owner", "Roman")
    @allure.feature("Функционал аутентификации пользователя.")
    @allure.title('Тест на успешный выход пользователя из своего аккаунта.')
    def test_logout_as_user(self, common_user_registered, super_admin):
        #\assert api_manager.session.headers['Authorization'] == f"Bearer {login_as_user_response['accessToken']}"
        assert common_user_registered.api.session.cookies['refresh_token'] == common_user_registered.refreshToken.get('refreshToken')

        common_user_registered.api.auth_api.logout()
        #assert 'Authorization' not in api_manager.session.headers
        #assert api_manager.session.headers['Authorization'] == ''
        assert ['refresh_token'] not in common_user_registered.api.session.cookies

        #super_admin.api.user_api.delete_user(common_user_registered.id)



    '''
    def test_refresh_tokens(self, common_user_created):
        initial_access_token = common_user_registered.api.session.headers['Authorization']
        initial_refresh_token = common_user_registered.api.session.cookies['refresh_token']

        refresh_tokens_response = common_user_created.api.auth_api.refresh_tokens()

        #assert refresh_tokens_response['accessToken'] != initial_access_token
        assert refresh_tokens_response['refreshToken'] != initial_refresh_token

        #assert api_manager.session.headers['Authorization'] == f"Bearer {refresh_tokens_response['accessToken']}"
        assert common_user_registered.api.session.cookies['refresh_token'] == refresh_tokens_response['refreshToken']
    '''

    @allure.tag("smoke", "regression")
    @allure.label("owner", "Roman")
    @allure.feature("Функционал аутентификации пользователя.")
    @allure.title('Тест на успешное обновление токена обновления пользователя.')
    def test_refresh_tokens(self, common_user_registered, super_admin):
        #initial_access_token = common_user_registered.api.session.headers['Authorization']
        initial_refresh_token = common_user_registered.api.session.cookies['refresh_token']

        refresh_tokens_response = common_user_registered.api.auth_api.refresh_tokens()

        # assert refresh_tokens_response['accessToken'] != initial_access_token
        assert refresh_tokens_response['refreshToken'] != initial_refresh_token

        # assert api_manager.session.headers['Authorization'] == f"Bearer {refresh_tokens_response['accessToken']}"
        assert common_user_registered.api.session.cookies['refresh_token'] == refresh_tokens_response['refreshToken']

       #super_admin.api.user_api.delete_user(common_user_registered.id)


    @allure.tag("smoke", "regression")
    @allure.label("owner", "Roman")
    @allure.feature("Функционал аутентификации пользователя.")
    @allure.title('Тест на аутентификацию с учеткой админа.')
    def test_login_as_admin(self, api_manager):
        login_as_admin_response = api_manager.auth_api.authenticate(UserData.get_admin_creds_for_authentication())

        assert 'id' in  login_as_admin_response['user'], 'В ответе отсутствует id админа.'
        assert 'ADMIN' in  login_as_admin_response['user']['roles'], 'У админа отсутствует роль ADMIN.'
        assert 'accessToken' in  login_as_admin_response, 'В ответе отсутствует токен доступа.'
        assert 'refreshToken' in login_as_admin_response, 'В ответе отсутствует токен обновления.'

        assert api_manager.session.headers['Authorization'] == f"Bearer {login_as_admin_response['accessToken']}", 'Токен доступа, который пришел в ответ на запрос авторизации, не установлен как токен доступа сессии.'
        assert api_manager.session.cookies['refresh_token'] == login_as_admin_response['refreshToken']


    @allure.tag("smoke", "regression")
    @allure.label("owner", "Roman")
    @allure.feature("Функционал работы с пользователем.")
    @allure.title('Тест на удаление пользователя.')
    def test_delete_user(self, common_user_created_without_deleting_user_after_test, super_admin):
        #user_data = vars(common_user_created_without_deleting_user_after_test)
        delete_user_response = common_user_created_without_deleting_user_after_test.api.user_api.delete_user(common_user_created_without_deleting_user_after_test.id)

        #assert delete_user_response['id'] == deleted_user_data['id'], 'id удаленного пользователя не совпадает с id пользователя, который должен был быть удален.'

        #super_admin.api.user_api.get_user_info(user_data, 404)


    @allure.tag("smoke", "regression")
    @allure.label("owner", "Roman")
    @allure.feature("Функционал работы с пользователем.")
    @allure.title('Тест на создание пользователя админом.')
    def test_create_user_as_admin(self, super_admin, fixture_user_data_for_creation_by_admin):
        fixture_user_data_for_creation_by_admin = fixture_user_data_for_creation_by_admin()
        create_user_response = super_admin.api.user_api.create_user_as_admin(fixture_user_data_for_creation_by_admin)

        assert 'id' in create_user_response, "ID пользователя отсутствует в ответе."
        assert create_user_response["email"] == fixture_user_data_for_creation_by_admin["email"], "Email не совпадает."
        assert create_user_response["fullName"] == fixture_user_data_for_creation_by_admin["fullName"], "Имя и фамилия не совпадает."
        assert create_user_response["roles"] == ['USER'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert create_user_response['verified'] == fixture_user_data_for_creation_by_admin["verified"], 'Зарегистрированный пользователь не верефицирован.'
        assert create_user_response['banned'] == fixture_user_data_for_creation_by_admin["banned"], 'Зарегистрированный пользователь забанен.'
        assert date.today().strftime('%Y-%m-%d') in create_user_response[
            'createdAt'], 'Дата регистрации пользователя не корректна.'

        get_created_user_response = super_admin.api.user_api.get_user_info(create_user_response)

        assert get_created_user_response['id'] == create_user_response['id'], 'ID пользователя не корректное.'
        assert get_created_user_response["email"] == fixture_user_data_for_creation_by_admin["email"], "Email не совпадает."
        assert get_created_user_response["fullName"] == fixture_user_data_for_creation_by_admin["fullName"], "Имя и фамилия не совпадает."
        assert get_created_user_response["roles"] == ['USER'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert get_created_user_response['verified'] == fixture_user_data_for_creation_by_admin["verified"], 'Зарегистрированный пользователь не верефицирован.'
        assert get_created_user_response['banned'] == fixture_user_data_for_creation_by_admin["banned"], 'Зарегистрированный пользователь забанен.'
        assert date.today().strftime('%Y-%m-%d') in get_created_user_response[
            'createdAt'], 'Дата регистрации пользователя не корректна.'

        super_admin.api.user_api.delete_user(create_user_response['id'])


    @allure.tag("smoke", "regression")
    @allure.label("owner", "Roman")
    @allure.feature("Функционал работы с пользователем.")
    @allure.title('Тест на изменение данных пользователя админом.')
    def test_change_user_as_admin(self, super_admin, fixture_user_data_for_creation_by_admin,
                                  fixture_test_user_created_by_admin_changed_data):
        fixture_user_data_for_creation_by_admin = fixture_user_data_for_creation_by_admin()

        create_user_response = super_admin.api.user_api.create_user_as_admin(fixture_user_data_for_creation_by_admin)

        change_user_response = super_admin.api.user_api.change_user_as_admin(create_user_response, fixture_test_user_created_by_admin_changed_data)

        assert change_user_response["email"] == fixture_test_user_created_by_admin_changed_data["email"], "Email не совпадает"
        assert change_user_response["banned"] == fixture_test_user_created_by_admin_changed_data["banned"], "Забенен ли пользователь не совпадает"
        #assert change_user_response['id'] == create_user_response['id'], 'ID пользователя не корректный.'
        assert change_user_response["fullName"] == create_user_response["fullName"], "Имя и фамилия не совпадает."
        assert change_user_response["roles"] == create_user_response['roles'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert change_user_response['verified'] == create_user_response['verified'], 'Зарегистрированный пользователь не верефицирован.'
        assert date.today().strftime('%Y-%m-%d') in change_user_response[
            'createdAt'], 'Дата регистрации пользователя отсутствует.'

        get_user_after_change_response = super_admin.api.user_api.get_user_info(create_user_response)

        assert get_user_after_change_response["email"] == fixture_test_user_created_by_admin_changed_data["email"], "Email не совпадает"
        assert get_user_after_change_response["banned"] == fixture_test_user_created_by_admin_changed_data["banned"], "Забенен ли пользователь не совпадает"
        assert get_user_after_change_response['id'] == create_user_response['id'], 'ID пользователя не корректное.'
        assert get_user_after_change_response["fullName"] ==  create_user_response["fullName"], "Имя и фамилия не совпадает."
        assert get_user_after_change_response["roles"] == create_user_response['roles'], 'Роль USER не присвоена зарегистрированному пользователю.'
        assert get_user_after_change_response['verified'] == create_user_response['verified'], 'Зарегистрированный пользователь не верефицирован.'
        assert date.today().strftime('%Y-%m-%d') in get_user_after_change_response[
            'createdAt'], 'Дата регистрации пользователя отсутствует.'

        super_admin.api.user_api.delete_user(create_user_response['id'])


    @allure.tag("smoke", "regression")
    @allure.label("owner", "Roman")
    @allure.feature("Функционал работы с пользователем.")
    @allure.title('Тест на получение данных всех пользователей с фильтрацией по роли.')
    def test_get_all_users_filtered_by_role(self, super_admin):
        role = Roles.ADMIN.value

        get_all_users_filtered_by_role_response = super_admin.api.user_api.get_all_users_filtered_by_role(role)

        for user in get_all_users_filtered_by_role_response['users']:
            assert role in user['roles'], 'В отфильтрованном по роли "Админ" списке пользователей по крайней мере у одного пользователя нет роли администратора.'



