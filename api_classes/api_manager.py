from api_classes.auth_api import AuthAPI
from api_classes.movies_api import MoviesAPI
from api_classes.payment_api import PaymentAPI
from api_classes.user_api import UserAPI


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.payment_api = PaymentAPI(session)
        self.movies_api = MoviesAPI(session)

    def close_session(self):
        self.session.close()