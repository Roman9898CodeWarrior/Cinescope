from pydantic import BaseModel

class RefreshTokenResponseModel(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int