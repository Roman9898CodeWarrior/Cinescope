from constants import AUTH_URL, PAYMENT_URL, CREATE_PAYMENT_ENDPOINT, USER_ENDPOINT, FIND_ALL_PAYMENTS_ENDPOINT
from custom_requester.custom_requester import CustomRequester

class PaymentAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=PAYMENT_URL)

    def create_payment(self, payment_data,  expected_status=201):
        create_payment_response = self.send_request(
            method="POST",
            endpoint=CREATE_PAYMENT_ENDPOINT,
            data=payment_data,
            expected_status=expected_status
        )

        return create_payment_response.json()

    def get_user_payments(self, expected_status=200):
        get_user_payments_response = self.send_request(
            method="GET",
            endpoint=USER_ENDPOINT,
            expected_status=expected_status
        )
        return get_user_payments_response.json()

    def get_another_user_payments_as_admin(self, user_id, expected_status=200):
        get_another_user_payments_as_admin_response = self.send_request(
            method="GET",
            endpoint=f'{USER_ENDPOINT}/{user_id}',
            expected_status=expected_status
        )

        return get_another_user_payments_as_admin_response.json()

    def get_all_payments_by_admin(self, params=None, expected_status=200):
        get_all_payments_by_admin_response = self.send_request(
            method="GET",
            endpoint=FIND_ALL_PAYMENTS_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

        return get_all_payments_by_admin_response.json()