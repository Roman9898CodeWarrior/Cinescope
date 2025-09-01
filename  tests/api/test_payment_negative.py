import pytest

class TestPaymentAPINegative:
    @pytest.mark.parametrize("card_param,param_non_valid_value", [
        ('cardNumber', "12345678"),
        ('securityCode', 3211)
    ])
    def test_try_to_create_payment_with_non_valid_card_data(self, common_user_registered,
                                                            fixture_payment, card_param, param_non_valid_value):
        valid_payment_data = fixture_payment()
        valid_payment_data['card'][card_param] = param_non_valid_value
        non_valid_payment_data = valid_payment_data
        create_payment_response= common_user_registered.api.payment_api.create_payment(non_valid_payment_data, 400)

        if card_param == 'cardNumber':
            assert 'card.Поле card.cardNumber должно содержать 16 цифр' in create_payment_response['message'], 'Сообщение об ошибке не корректное.'
        elif card_param == 'securityCode':
            assert 'card.Поле card.securityCode должно быть меньше 1000' in create_payment_response['message'], 'Сообщение об ошибке не корректное.'

    def test_try_to_create_payment_without_authorisation(self, api_manager, fixture_payment):
        api_manager.payment_api.create_payment(fixture_payment(), 401)

    def test_try_to_get_all_users_payments_as_user(self, common_user_created):
        common_user_created.api.payment_api.get_all_payments_by_admin(expected_status=403)

    def test_try_to_get_another_user_payments_as_admin_with_wrong_user_id(self, super_admin):
        get_user_payments_response = super_admin.api.payment_api.get_another_user_payments_as_admin(111111111122222222233333333333, 404)

        assert get_user_payments_response['message'] == 'Пользователь не найден', 'Статус в теле ответа не корректный'

    def test_try_to_get_another_user_payments_as_user(self, common_user_registered, common_user_created,
                                                      fixture_payment):
        first_user_id = common_user_registered.id

        common_user_registered.api.payment_api.create_payment(fixture_payment())

        get_registered_user_payments_response = common_user_created.api.payment_api.get_another_user_payments_as_admin(first_user_id, 403)
        response_message = get_registered_user_payments_response['message']

        assert response_message == 'Forbidden resource', f'Ожидался статус "Forbidden resource", а пришел {response_message}.'

    def test_try_to_get_all_payments_filtered_by_wrong_payment_status_as_admin(self, super_admin):
        get_all_payments_as_admin_response = super_admin.api.payment_api.get_all_payments_by_admin({'status': 'INVALID_CARDS'}, 400)
        response_message = get_all_payments_as_admin_response['message'][0]

        assert response_message == 'Поле status имеет недопустимое значение', f'Ожидался статус , а пришел {response_message}.'