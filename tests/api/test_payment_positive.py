from datetime import datetime


class TestPaymentAPIPositive:
    def test_create_payment(self, fixture_payment, common_user_registered, super_admin):
        create_payment_response = common_user_registered.api.payment_api.create_payment(fixture_payment())
        assert create_payment_response['status'] == 'SUCCESS', 'Статус в теле ответа не корректный.'

        #super_admin.api.user_api.delete_user(common_user_registered.id)


    def test_get_user_payments(self, fixture_payment, common_user_registered, super_admin):
        payment_data = fixture_payment()
        common_user_registered.api.payment_api.create_payment(payment_data)
        movie_id = payment_data['movieId']
        user_id = common_user_registered.id

        get_user_payments_response = common_user_registered.api.payment_api.get_user_payments()

        assert get_user_payments_response['root'][0].movieId == movie_id, 'id фильма не совпадает.'
        assert get_user_payments_response['root'][0].userId == user_id, 'id пользователя не совпадает'

        #super_admin.api.user_api.delete_user(common_user_registered.id)


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


    def test_get_another_user_payments_as_admin(self, super_admin, common_user_registered, fixture_payment):
        payment_data = fixture_payment()
        common_user_registered.api.payment_api.create_payment(payment_data)
        movie_id = payment_data['movieId']
        user_id = common_user_registered.id

        get_user_payments_response = super_admin.api.payment_api.get_another_user_payments_as_admin(user_id)

        assert get_user_payments_response['root'][0].movieId == movie_id, 'id фильма не совпадает.'
        assert get_user_payments_response['root'][0].userId == user_id, 'id пользователя не совпадает'

        #super_admin.api.user_api.delete_user(common_user_registered.id)


    def test_get_all_payments_as_admin(self, common_user_registered, super_admin, fixture_payment):
        payment_data_1 = fixture_payment()
        payment_data_2 = fixture_payment()
        payment_data_3 = fixture_payment()

        payment1_movie_id = payment_data_1['movieId']
        payment2_movie_id = payment_data_2['movieId']
        payment3_movie_id = payment_data_3['movieId']
        user_id = common_user_registered.id

        common_user_registered.api.payment_api.create_payment(payment_data_1)
        common_user_registered.api.payment_api.create_payment(payment_data_2)
        common_user_registered.api.payment_api.create_payment(payment_data_3)

        get_all_payments_as_admin_response = super_admin.api.payment_api.get_all_payments_by_admin()

        assert get_all_payments_as_admin_response['payments'][0]['movieId'] == payment3_movie_id, 'id фильма не совпадает.'
        assert get_all_payments_as_admin_response['payments'][0]['userId'] == user_id, 'id пользователя не совпадает'
        assert get_all_payments_as_admin_response['payments'][1]['movieId'] == payment2_movie_id, 'id фильма не совпадает.'
        assert get_all_payments_as_admin_response['payments'][1]['userId'] == user_id, 'id пользователя не совпадает'''
        assert get_all_payments_as_admin_response['payments'][2]['movieId'] == payment1_movie_id, 'id фильма не совпадает.'
        assert get_all_payments_as_admin_response['payments'][2]['userId'] == user_id, 'id пользователя не совпадает'''

        #super_admin.api.user_api.delete_user(common_user_registered.id)


    def test_get_all_payments_filtered_by_payment_status_as_admin(self, super_admin):
        get_all_payments_by_admin_response = super_admin.api.payment_api.get_all_payments_by_admin({'status': 'INVALID_CARD'})

        for payment in get_all_payments_by_admin_response['payments']:
            assert payment['status'] == 'INVALID_CARD', 'В отфильтрованном по статусу INVALID_CARD списке платежей по крайней мере у одного платежа статус другой.'


    def test_get_all_payments_sorted_by_creation_time_desc_as_admin (self, common_user_registered,
                                                                     fixture_payment, super_admin):
        payment_data_1 = fixture_payment()
        payment_data_2 = fixture_payment()

        first_payment_movie_id = payment_data_1['movieId']
        second_payment_movie_id = payment_data_2['movieId']

        common_user_registered.api.payment_api.create_payment(payment_data_1)
        common_user_registered.api.payment_api.create_payment(payment_data_2)

        get_payments_sorted_by_desc_first_page_response = super_admin.api.payment_api.get_all_payments_by_admin({'page': 1, 'pageSize': 20, 'createdAt': 'desc'})

        assert get_payments_sorted_by_desc_first_page_response['payments'][0]['movieId'] == second_payment_movie_id, 'id фильма не совпадает.'
        assert get_payments_sorted_by_desc_first_page_response['payments'][1]['movieId'] == first_payment_movie_id, 'id пользователя не совпадает'

        oldest_payment_date = datetime.now()
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        for payment in get_payments_sorted_by_desc_first_page_response['payments']:
            date_of_creation = datetime.strptime(payment['createdAt'], date_format)
            if date_of_creation < oldest_payment_date:
                oldest_payment_date = date_of_creation

        assert datetime.strptime(get_payments_sorted_by_desc_first_page_response['payments'][19]['createdAt'], date_format) == oldest_payment_date

        #super_admin.api.user_api.delete_user(common_user_registered.id)


    def test_get_all_payments_sorted_by_creation_time_asc_as_admin(self, super_admin):
        get_all_payments_sorted_by_asc_response = super_admin.api.payment_api.get_all_payments_by_admin({'createdAt': 'asc'})

        oldest_payment_date = datetime.now()
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        for payment in get_all_payments_sorted_by_asc_response['payments']:
            date_of_creation = datetime.strptime(payment['createdAt'], date_format)
            if date_of_creation < oldest_payment_date:
                oldest_payment_date = date_of_creation

        assert datetime.strptime(get_all_payments_sorted_by_asc_response['payments'][0]['createdAt'],
                                 date_format) == oldest_payment_date




