from utils.data_generator import DataGenerator


class PaymentData:
    @staticmethod
    def get_valid_payment_data():
        movie_id = DataGenerator.get_movie_id()
        amount = DataGenerator.generate_random_amount()
        card_holder_name = DataGenerator.generate_random_name()

        return {
            "movieId": movie_id,
            "amount": amount,
            "card": {
                "cardNumber": "4242424242424242",
                "cardHolder": card_holder_name,
                "expirationDate": "12/25",
                "securityCode": 123
            }
        }

    @staticmethod
    def get_non_valid_payment_data():
        movie_id = DataGenerator.get_movie_id()
        amount = DataGenerator.generate_random_amount()
        card_holder_name = DataGenerator.generate_random_name()

        return {
            "movieId": movie_id,
            "amount": amount,
            "card": {
                "cardNumber": "4242424242424242",
                "cardHolder": card_holder_name,
                "expirationDate": "12/25",
                "securityCode": 321
            }
        }