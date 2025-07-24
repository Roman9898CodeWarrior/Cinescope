import requests

from constants import BASE_URL, CREATE_PAYMENT, USER_ENDPOINT

class TestPaymentAPIPositive:
    def test_create_payment(self, auth_session, payment_data):
        request_url = f'{BASE_URL}/{CREATE_PAYMENT}'
        create_payment_response = auth_session.post(request_url, json=payment_data)

        assert create_payment_response == 201, 'Платеж не создан.'
        assert not create_payment_response.json(), 'Платеж не создан.'

    def test_get_user_payments(self, auth_session, payment_data):
        create_payment_url = f'{BASE_URL}/{CREATE_PAYMENT}'
        get_user_payments_url = f'{BASE_URL}/{USER_ENDPOINT}'
        movie_id = payment_data['movieId']

        create_payment_response = auth_session.post(create_payment_url, json=payment_data)

        assert create_payment_response == 201, 'Платеж не создан.'

        get_user_payments_responce = auth_session.get(get_user_payments_url)

        assert get_user_payments_responce.status_code == 200, 'Платеж не найден.'
        assert get_user_payments_responce.json()[0]['id'] == movie_id, 'id фильма не совпадает.'

    def test_get_any_user_payments_by_admin(self, auth_session, admin_auth, payment_data):
        create_payment_url = f'{BASE_URL}/{CREATE_PAYMENT}'
        get_user_payments_url = f'{BASE_URL}/{USER_ENDPOINT}'
        movie_id = payment_data['movieId']

        create_payment_response = auth_session.post(create_payment_url, json=payment_data)

        assert create_payment_response == 201, 'Платеж не создан.'

        get_user_payments_by_admin_responce = auth_session.get(get_user_payments_url)



