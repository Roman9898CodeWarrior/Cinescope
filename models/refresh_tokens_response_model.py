from pydantic import BaseModel

class RefreshTokensResponse(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int