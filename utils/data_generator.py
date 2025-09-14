import random
import string
from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_valid_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_non_valid_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}gmail.com"

    @staticmethod
    def get_movie_id():
        return random.choice([2365, 2364, 2361, 2360, 2359, 2358, 2355, 2354, 2353])

    @staticmethod
    def generate_random_amount():
        return faker.random_int(1, 5)

    @staticmethod
    def generate_random_card_number():
        return "".join(random.choices("0123456789", k=16))

    @staticmethod
    def generate_non_valid_random_card_number():
        return "".join(random.choices("0123456789", k=15))

    @staticmethod
    def generate_random_expiration_date():
        return f"{random.randint(1, 12):02}/{faker.random_int(25, 35)}"

    @staticmethod
    def generate_random_security_code():
        return faker.random_int(0, 999)

    @staticmethod
    def generate_random_int():
        return faker.random_int(1, 25000)

    @staticmethod
    def get_random_first_name():
        return faker.first_name()

    @staticmethod
    def get_random_last_name():
        return faker.first_name()

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_valid_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        upper_case_letter = random.choice(string.ascii_uppercase)  # Одна буква
        lower_case_letter = random.choice(string.ascii_lowercase)
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(5, 17)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(upper_case_letter + digits + lower_case_letter + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_non_valid_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        letters = random.choice(string.ascii_uppercase) + random.choice(string.ascii_lowercase)
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))
        password = list(letters + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def get_valid_phone_number():
        return faker.msisdn()

if __name__ == "__main__":
    print(DataGenerator.get_valid_phone_number())

