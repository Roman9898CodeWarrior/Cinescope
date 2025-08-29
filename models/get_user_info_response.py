from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, field_validator

from constants.roles import Roles


class RegisterCreateGetOrDeleteUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: List[Roles]
    verified: bool
    createdAt: str
    banned: bool

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value
