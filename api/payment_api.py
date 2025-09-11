from venv import logger

import allure
import pytest
from pydantic import ValidationError

from constants.constants import PAYMENT_URL, CREATE_PAYMENT_ENDPOINT, USER_ENDPOINT, FIND_ALL_PAYMENTS_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from models.api_models.get_user_payments_response_model import UserPaymentsResponseModel
from models.api_models.payment_data_model import DataForPaymentCreationModel


class PaymentAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session, PAYMENT_URL)

    @allure.step('Создание платежа.')
    def create_payment(self, payment_data,  expected_status=201):
        try:
            payment_data_validated = vars(DataForPaymentCreationModel(**payment_data))
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

        create_payment_response = self.send_request(
            method="POST",
            endpoint=CREATE_PAYMENT_ENDPOINT,
            data=payment_data_validated,
            expected_status=expected_status
        )

        return create_payment_response.json()

    @allure.step('Создание платежа без валидации данных для объекта платежа.')
    def create_payment_without_payment_data_validation(self, payment_data,  expected_status=201):
        create_payment_response = self.send_request(
            method="POST",
            endpoint=CREATE_PAYMENT_ENDPOINT,
            data=payment_data,
            expected_status=expected_status
        )

        return create_payment_response.json()

    @allure.step('Получение платежей пользователя самим пользователем.')
    def get_user_payments(self, expected_status=200):
        get_user_payments_response = self.send_request(
            method="GET",
            endpoint=USER_ENDPOINT,
            expected_status=expected_status
        )

        if expected_status != 200 and get_user_payments_response.status_code != 200:
            return get_user_payments_response
        else:
            try:
                get_user_payments_response_validated = vars(UserPaymentsResponseModel.model_validate(get_user_payments_response.json()))
                return get_user_payments_response_validated
            except ValidationError as e:
                pytest.fail(f'Ошибка валидации: {e}')
                logger.info(f'Ошибка валидации: {e}')

    @allure.step('Получение платежей другого пользователя админом.')
    def get_another_user_payments_as_admin(self, user_id, expected_status=200):
        get_another_user_payments_as_admin_response = self.send_request(
            method="GET",
            endpoint=f'{USER_ENDPOINT}/{user_id}',
            expected_status=expected_status
        )

        if expected_status != 200 and get_another_user_payments_as_admin_response.status_code != 200:
            return get_another_user_payments_as_admin_response.json()
        else:
            try:
                get_another_user_payments_as_admin_response = vars(
                    UserPaymentsResponseModel.model_validate(get_another_user_payments_as_admin_response.json()))
                return get_another_user_payments_as_admin_response
            except ValidationError as e:
                pytest.fail(f'Ошибка валидации: {e}')
                logger.info(f'Ошибка валидации: {e}')

    @allure.step('Получение платежей всех пользователей админом.')
    def get_all_payments_by_admin(self, params=None, expected_status=200):
        get_all_payments_by_admin_response = self.send_request(
            method="GET",
            endpoint=FIND_ALL_PAYMENTS_ENDPOINT,
            params=params,
            expected_status=expected_status
        )

        return get_all_payments_by_admin_response.json()