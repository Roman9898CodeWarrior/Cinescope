from utils.data_generator import DataGenerator


class DemoQaData:
    @staticmethod
    def get_valid_data_for_student_registration():
        first_name = DataGenerator.get_random_first_name()
        last_name = DataGenerator.get_random_last_name()
        email = DataGenerator.generate_valid_random_email()
        phone_number = DataGenerator.get_valid_phone_number()

        return {
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'gender': 'Male',
            'phoneNumber': phone_number,
            'date_of_birth': '24 September,2025',
            'subjects': ['Computer Science'],
            'hobbies': ['Reading'],
            'pictureFileName': 'trace_2025-09-09_17-46-16.zip',
            'currentAddress': 'bogorodsk',
            'state': 'Uttar Pradesh',
            'city': 'Merrut'
        }