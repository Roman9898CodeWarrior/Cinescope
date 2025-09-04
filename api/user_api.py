from venv import logger

import allure
import pytest
from pydantic import ValidationError

from constants.constants import USER_ENDPOINT, AUTH_URL
from custom_requester.custom_requester import CustomRequester
from models.get_all_users_response_model import AllUsers
from models.get_user_info_response_model import RegisterCreateGetOrDeleteUserResponse, ChangeUserResponse
from models.user_data_model import UserDataForCreationByAdmin


class UserAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session, AUTH_URL)
    '''
    def __init__(self, session):
        super().__init__(session, AUTH_URL)
    '''

    @allure.step('Получение данных пользователя.')
    def get_user_info(self, user_data, expected_status=200):
        registered_user_id = user_data['id']

        get_user_response = self.send_request(
            method="GET",
            endpoint=f'{USER_ENDPOINT}/{registered_user_id}',
            expected_status=expected_status
        )

        if expected_status != 200 and get_user_response.status_code != 200:
            return get_user_response.json()
        else:
            try:
                get_user_response_validated = vars(RegisterCreateGetOrDeleteUserResponse(**get_user_response.json()))
                return get_user_response_validated
            except ValidationError as e:
                pytest.fail(f'Ошибка валидации: {e}')
                logger.info(f'Ошибка валидации: {e}')

    @allure.step('Создание пользователя админом.')
    def create_user_as_admin(self, user_data_for_creation_by_admin, expected_status=201):
        user_data_for_creation = {}

        try:
            user_data_for_creation = vars(UserDataForCreationByAdmin(**user_data_for_creation_by_admin))
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

        create_user_response = self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=user_data_for_creation,
            expected_status=expected_status
        )

        if expected_status != 200 and create_user_response.status_code != 200:
            return create_user_response.json()
        else:
            try:
                create_user_response_validated = vars(RegisterCreateGetOrDeleteUserResponse(**create_user_response.json()))
                return create_user_response_validated
            except ValidationError as e:
                pytest.fail(f'Ошибка валидации: {e}')
                logger.info(f'Ошибка валидации: {e}')

    @allure.step('Изменение данных пользователя админом.')
    def change_user_as_admin(self, test_user_created_by_admin, test_user_created_by_admin_changed_data, expected_status=200):
        created_user_id = test_user_created_by_admin['id']

        change_user_response = self.send_request(
            method="PATCH",
            endpoint=f'{USER_ENDPOINT}/{created_user_id}',
            data=test_user_created_by_admin_changed_data,
            expected_status=expected_status
        )

        if expected_status != 200 and change_user_response.status_code != 200:
            return change_user_response.json()
        try:
            change_user_response_validated = vars(ChangeUserResponse(**change_user_response.json()))
            return change_user_response_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

    @allure.step('Удаление пользователя.')
    def delete_user(self, user_id, expected_status=200):
        delete_user_response = self.send_request(
            method="DELETE",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            expected_status=expected_status
        )

        '''
        try:
            delete_user_response_validated = vars(RegisterCreateGetOrDeleteUserResponse(**delete_user_response.json()))
            return delete_user_response_validated
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')
        '''

    @allure.step('Получение админом данных по всем пользователям с фильтрацией по роли пользователя.')
    def get_all_users_filtered_by_role(self, role, expected_status=200):
        get_all_users_filtered_by_role_response = self.send_request(
            method="GET",
            endpoint=USER_ENDPOINT,
            params={'roles': {role}},
            expected_status=expected_status
        )

        try:
            get_all_users_filtered_by_role_response = vars(AllUsers(**get_all_users_filtered_by_role_response.json()))
            return get_all_users_filtered_by_role_response
        except ValidationError as e:
            pytest.fail(f'Ошибка валидации: {e}')
            logger.info(f'Ошибка валидации: {e}')

