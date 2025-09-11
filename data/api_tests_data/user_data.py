from constants.roles import Roles
from resources.creds import SuperAdminCreds
from utils.data_generator import DataGenerator


class UserData:
    @staticmethod
    def get_user_data_for_registration():
        random_email = DataGenerator.generate_valid_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_valid_random_password()

        return {
            "email": random_email,
            "fullName": random_name,
            "password": random_password,
            "passwordRepeat": random_password,
            "roles": [Roles.USER.value]
        }

    @staticmethod
    def get_non_valid_user_data_for_registration():
        random_email = DataGenerator.generate_valid_random_email()
        random_name = DataGenerator.generate_random_name()
        random_non_valid_password = DataGenerator.generate_non_valid_random_password()

        return {
            "email": random_email,
            "fullName": random_name,
            "password": random_non_valid_password,
            "passwordRepeat": random_non_valid_password,
            "roles": [Roles.USER.value]
        }

    @staticmethod
    def get_user_data_for_creation_by_admin():
        random_email = DataGenerator.generate_valid_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_valid_random_password()

        return {
            "email": random_email,
            "fullName": random_name,
            "password": random_password,
            "verified": True,
            "banned": False
        }

    @staticmethod
    def get_user_data_for_change_by_admin():
        random_email = DataGenerator.generate_valid_random_email()

        return {
            "email": random_email,
            "banned": True
        }

    @staticmethod
    def get_admin_creds_for_authentication():
        return {
            "email": SuperAdminCreds.EMAIL,
            "password": SuperAdminCreds.PASSWORD
        }