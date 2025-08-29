from typing import List

from pydantic import BaseModel, Field

from constants.roles import Roles

class User(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: List[Roles]

class LogInResponse(BaseModel):
    user: User
    accessToken: str
    refreshToken: str
    expiresIn: int

