from constants.constants import USER_ENDPOINT, AUTH_URL
from custom_requester.custom_requester import CustomRequester

class UserAPI(CustomRequester):
    def __init__(self, session):
        self.session = session
        super().__init__(session, AUTH_URL)
    '''
    def __init__(self, session):
        super().__init__(session, AUTH_URL)
    '''

    def get_user_info(self, user_data, expected_status=200):
        #api_manager.auth_api.login_as_admin()
        registered_user_id = user_data['id']

        get_user_response = self.send_request(
            method="GET",
            endpoint=f'{USER_ENDPOINT}/{registered_user_id}',
            expected_status=expected_status
        )

        return get_user_response.json()

    def create_user_as_admin(self, user_data_for_creation_by_admin, expected_status=201):
        #api_manager.auth_api.login_as_admin()

        create_user_response = self.send_request(
            method="POST",
            endpoint=USER_ENDPOINT,
            data=user_data_for_creation_by_admin,
            expected_status=expected_status
        )

        return create_user_response.json()

    def change_user_as_admin(self, test_user_created_by_admin, test_user_created_by_admin_changed_data, expected_status=200):
        #api_manager.auth_api.login_as_admin()

        created_user_id = test_user_created_by_admin['id']

        change_user_response = self.send_request(
            method="PATCH",
            endpoint=f'{USER_ENDPOINT}/{created_user_id}',
            data=test_user_created_by_admin_changed_data,
            expected_status=expected_status
        )

        return change_user_response.json()


    def delete_user(self, user_data, expected_status=200):
        delete_user_response = self.send_request(
            method="DELETE",
            endpoint=f"{USER_ENDPOINT}/{user_data['user']['id']}",
            expected_status=expected_status
        )

        return delete_user_response.json()

    def get_all_users_filtered_by_role(self, role, expected_status=200):
        #api_manager.auth_api.login_as_admin()

        get_all_users_filtered_by_role_response = self.send_request(
            method="GET",
            endpoint=USER_ENDPOINT,
            params={f'roles': {role}},
            expected_status=expected_status
        )

        return get_all_users_filtered_by_role_response.json()
