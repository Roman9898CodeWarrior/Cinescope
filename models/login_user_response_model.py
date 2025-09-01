from typing import Any

from pydantic import BaseModel, Field, field_validator

from constants.roles import Roles

class User(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: list[Roles]

    @field_validator("roles")
    def from_enum_to_str(cls, value: list[Roles]) -> list[str]:
        new_list = []
        for role in value:
            new_list.append(role.value)
        value = new_list
        return value

    class Config:
        json_encoders = {
            Roles: lambda v: v.value
        }

class LogInResponse(BaseModel):
    user: User
    accessToken: str
    refreshToken: str
    expiresIn: int

    @field_validator("user")
    def from_object_to_dict(cls, value: User) -> dict[str, Any] | None:
        return vars(value)

