from datetime import datetime
from constants import PAYMENT_URL, CREATE_PAYMENT_ENDPOINT, USER_ENDPOINT, AUTH_URL, REGISTER_ENDPOINT, HEADERS, FIND_ALL_PAYMENTS_ENDPOINT


class TestPaymentAPIPositive:
    def test_create_payment(self, api_manager, fixture_payment_data, fixture_login_as_user):
        create_payment_response = api_manager.payment_api.create_payment(fixture_payment_data())
        assert create_payment_response.json()['status'] == 'SUCCESS', 'Статус в теле ответа не корректный.'

    def test_get_user_payments(self, api_manager, fixture_login_as_user, fixture_create_payment):
        movie_id = fixture_create_payment()['movieId']
        user_id = fixture_login_as_user['user']['id']

        get_user_payments_response= api_manager.payment_api.get_user_payments()

        assert get_user_payments_response[0]['movieId'] == movie_id, 'id фильма не совпадает.'
        assert get_user_payments_response[0]['userId'] == user_id, 'id пользователя не совпадает'
    '''
    def test_get_any_user_payments_as_admin(self, payment_requester, fixture_login_as_user, fixture_create_payment, request):
        movie_id = fixture_create_payment()['movieId']
        user_id = fixture_login_as_user['user']['id']

        request.getfixturevalue('login_as_admin')

        get_user_payments_response = payment_requester.send_request(
            method="GET",
            endpoint=f'{USER_ENDPOINT}/{user_id}'
        )
        get_user_payments_response_data = get_user_payments_response.json()

        assert get_user_payments_response_data[0]['movieId'] == movie_id, 'id фильма не совпадает.'
        assert get_user_payments_response_data[0]['userId'] == user_id, 'id пользователя не совпадает'
    '''

    def test_get_another_user_payments_as_admin(self, api_manager, fixture_login_as_user, fixture_create_payment, request):
        movie_id = fixture_create_payment()['movieId']
        user_id = fixture_login_as_user['user']['id']

        request.getfixturevalue('login_as_admin')

        get_user_payments_response = api_manager.payment_api.get_another_user_payments_as_admin(user_id)

        assert get_user_payments_response[0]['movieId'] == movie_id, 'id фильма не совпадает.'
        assert get_user_payments_response[0]['userId'] == user_id, 'id пользователя не совпадает'

    def test_get_all_payments_as_admin(self, api_manager, fixture_login_as_user, fixture_create_payment):
        payment1 = fixture_create_payment()
        payment2 = fixture_create_payment()
        payment3 = fixture_create_payment()

        payment1_movie_id = payment1['movieId']
        payment2_movie_id = payment2['movieId']
        payment3_movie_id = payment3['movieId']

        user_id = fixture_login_as_user['user']['id']

        api_manager.auth_api.login_as_admin()

        get_all_payments_by_admin_response = api_manager.payment_api.get_all_payments_by_admin()

        assert get_all_payments_by_admin_response['payments'][0]['movieId'] == payment3_movie_id, 'id фильма не совпадает.'
        assert get_all_payments_by_admin_response['payments'][0]['userId'] == user_id, 'id пользователя не совпадает'
        assert get_all_payments_by_admin_response['payments'][1]['movieId'] == payment2_movie_id, 'id фильма не совпадает.'
        assert get_all_payments_by_admin_response['payments'][1]['userId'] == user_id, 'id пользователя не совпадает'''
        assert get_all_payments_by_admin_response['payments'][2]['movieId'] == payment1_movie_id, 'id фильма не совпадает.'
        assert get_all_payments_by_admin_response['payments'][2]['userId'] == user_id, 'id пользователя не совпадает'''

    def test_get_all_payments_filtered_by_payment_status_as_admin(self, api_manager):
        api_manager.auth_api.login_as_admin()

        get_all_payments_by_admin_response = api_manager.payment_api.get_all_payments_by_admin({'status': 'INVALID_CARD'})

        for payment in get_all_payments_by_admin_response['payments']:
            assert payment['status'] == 'INVALID_CARD', 'В отфильтрованном по статусу INVALID_CARD списке платежей по крайней мере у одного платежа статус другой.'

    def test_get_all_payments_sorted_by_creation_time_desc_as_admin (self, api_manager, fixture_login_as_user,
                                                                     fixture_create_payment):
        payment1 = fixture_create_payment()
        payment2 = fixture_create_payment()

        first_payment_movie_id = payment1['movieId']
        second_payment_movie_id = payment2['movieId']
        user_id = fixture_login_as_user['user']['id']

        api_manager.auth_api.login_as_admin()

        get_all_payments_sorted_by_desc_response = api_manager.payment_api.get_all_payments_by_admin({'pageSize': 1000, 'createdAt': 'desc'})

        all_payments_sorted_by_desc_count = len(get_all_payments_sorted_by_desc_response['payments'])
        assert get_all_payments_sorted_by_desc_response['payments'][0]['movieId'] == second_payment_movie_id, 'id фильма не совпадает.'
        assert get_all_payments_sorted_by_desc_response['payments'][1]['movieId'] == first_payment_movie_id, 'id пользователя не совпадает'
        assert get_all_payments_sorted_by_desc_response['payments'][0]['userId'] == user_id, 'id пользователя не совпадает'
        assert get_all_payments_sorted_by_desc_response['payments'][1]['userId'] == user_id, 'id пользователя не совпадает'

        oldest_payment_date = datetime.now()
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        for payment in get_all_payments_sorted_by_desc_response['payments']:
            date_of_creation = datetime.strptime(payment['createdAt'], date_format)
            if date_of_creation < oldest_payment_date:
                oldest_payment_date = date_of_creation

        assert datetime.strptime(get_all_payments_sorted_by_desc_response['payments'][all_payments_sorted_by_desc_count - 1]['createdAt'], date_format) == oldest_payment_date

        get_all_payments_sorted_by_asc_response = api_manager.payment_api.get_all_payments_by_admin({'pageSize': 1000, 'createdAt': 'asc'})

        assert datetime.strptime(get_all_payments_sorted_by_asc_response['payments'][0]['createdAt'],
                                 date_format) == oldest_payment_date

    def test_get_all_payments_sorted_by_creation_time_asc_as_admin(self, api_manager):
        api_manager.auth_api.login_as_admin()

        get_all_payments_sorted_by_asc_response = api_manager.payment_api.get_all_payments_by_admin({'pageSize': 1000, 'createdAt': 'asc'})

        oldest_payment_date = datetime.now()
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        for payment in get_all_payments_sorted_by_asc_response['payments']:
            date_of_creation = datetime.strptime(payment['createdAt'], date_format)
            if date_of_creation < oldest_payment_date:
                oldest_payment_date = date_of_creation

        assert datetime.strptime(get_all_payments_sorted_by_asc_response['payments'][0]['createdAt'],
                                 date_format) == oldest_payment_date




