import requests

from constants import PAYMENT_URL, CREATE_PAYMENT_ENDPOINT, USER_ENDPOINT, AUTH_URL, REGISTER_ENDPOINT, HEADERS, FIND_ALL_PAYMENTS_ENDPOINT
from utils.data_generator import faker


class TestPaymentAPINegative:
    def test_try_to_create_payment_with_non_valid_card_data(self, api_manager, fixture_login_as_user,
                                                            fixture_non_valid_payment_data):
        create_payment_response= api_manager.payment_api.create_payment(fixture_non_valid_payment_data(), 400)


        assert create_payment_response['error']['status'] == 'INVALID_CARD', 'Статус в теле ответа не корректный.'

    def test_try_to_create_payment_without_authorisation(self, api_manager, fixture_payment_data):
        api_manager.payment_api.create_payment(fixture_payment_data(), 401)

    def test_try_to_get_all_users_payments_as_user(self, api_manager, fixture_login_as_user):
        api_manager.payment_api.get_all_payments_by_admin(expected_status=403)

    def test_try_to_get_another_user_payments_as_admin_with_wrong_user_id(self, api_manager):
        api_manager.auth_api.login_as_admin()

        get_user_payments_response = api_manager.payment_api.get_another_user_payments_as_admin(111111111122222222233333333333, 404)

        assert get_user_payments_response.json()['message'] == 'Пользователь не найден'

    def test_try_to_get_another_user_payments_as_user(self, api_manager, fixture_height_order_login_as_user_function,
                                              fixture_payment_data):
        first_user_session = fixture_height_order_login_as_user_function()
        first_user_id = first_user_session['user']['id']

        api_manager.payment_api.create_payment(fixture_payment_data())

        fixture_height_order_login_as_user_function()

        get_first_user_payments_response = api_manager.payment_api.get_another_user_payments_as_admin(first_user_id, 403)
        response_message = get_first_user_payments_response['message']

        assert response_message == 'Forbidden resource', f'Ожидался статус "Forbidden resource", а пришел {response_message}.'

    def test_try_to_get_all_payments_filtered_by_wrong_payment_status_as_admin(self, api_manager):
        api_manager.auth_api.login_as_admin()

        get_all_payments_by_admin_response = api_manager.payment_api.get_all_payments_by_admin({'status': 'INVALID_CARDS'}, 400)
        response_message = get_all_payments_by_admin_response['message'][0]

        assert response_message == 'Поле status имеет недопустимое значение', f'Ожидался статус , а пришел {response_message}.'