from pydantic import BaseModel

class RefreshTokensResponseModel(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int