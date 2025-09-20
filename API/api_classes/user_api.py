import allure

from constants.constants import USER_ENDPOINT, AUTH_URL
from API.custom_requester import CustomRequester
from utils.data_validator import DataValidator


class UserAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session, AUTH_URL)


    @allure.step('Получение данных пользователя.')
    def get_user_info(self, user_data, expected_status=200):
        registered_user_id = user_data['id']

        get_user_data_response = self.send_request(
            method="GET",
            endpoint=f'{USER_ENDPOINT}/{registered_user_id}',
            expected_status=expected_status
        )

        if expected_status != 200 and get_user_data_response.status_code != 200:
            return get_user_data_response.json()
        else:
            get_user_response_data_validated = DataValidator.validate_registration_creation_delete_or_getuserdata_response_data(get_user_data_response)
            return get_user_response_data_validated

    @allure.step('Создание пользователя админом.')
    def create_user_as_admin(self, data_for_creation_user_by_admin, expected_status=201):
        data_for_creation_user_by_admin_validated = DataValidator.validate_data_for_creation_user_by_admin(data_for_creation_user_by_admin)

        create_user_response = self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=data_for_creation_user_by_admin_validated,
            expected_status=expected_status
        )

        if expected_status != 200 and create_user_response.status_code != 200:
            return create_user_response.json()
        else:
            create_user_response_data_validated = DataValidator.validate_registration_creation_delete_or_getuserdata_response_data(create_user_response)
            return create_user_response_data_validated

    @allure.step('Изменение данных пользователя админом.')
    def change_user_data_as_admin(self, test_user_created_by_admin, test_user_created_by_admin_changed_data, expected_status=200):
        created_user_id = test_user_created_by_admin['id']

        change_user_data_response = self.send_request(
            method="PATCH",
            endpoint=f'{USER_ENDPOINT}/{created_user_id}',
            data=test_user_created_by_admin_changed_data,
            expected_status=expected_status
        )

        if expected_status != 200 and change_user_data_response.status_code != 200:
            return change_user_data_response.json()
        else:
            change_user_data_response_data_validated = DataValidator.validate_change_user_data_response_data(change_user_data_response)
            return change_user_data_response_data_validated

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
        get_all_users_data_filtered_by_user_role_response = self.send_request(
            method="GET",
            endpoint=USER_ENDPOINT,
            params={'roles': {role}},
            expected_status=expected_status
        )

        get_all_users_filtered_by_user_role_response_data_validated = DataValidator.validate_get_all_users_data_response_data(get_all_users_data_filtered_by_user_role_response)
        return get_all_users_filtered_by_user_role_response_data_validated

