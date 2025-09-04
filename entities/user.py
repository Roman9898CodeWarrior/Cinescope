from api.api_manager import ApiManager


class CommonUser:
    def __init__(self, email: str, password: str, fullname: str, id: str, roles: list, created_at: str, verified: bool, banned: bool, api: ApiManager, access_token: str = None, refresh_token: str = None):
        self.email = email
        self.password = password
        self.fullname = fullname
        self.id = id
        self.roles = roles
        self.createdAt =created_at
        self.verified = verified
        self.banned = banned
        self.api = api
        self.accessToken = access_token if access_token is not None else {}
        self.refreshToken = refresh_token if refresh_token is not None else {}

    def __setitem__(self, key, value):
        if key == 'accessToken':
            self.accessToken[key] = value
        elif key == 'refreshToken':
            self.refreshToken[key] = value

    @property
    def creds(self):
        return self.email, self.password

class AdminUser:
    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self):
        return {
                "email": self.email,
                "password": self.password
                }