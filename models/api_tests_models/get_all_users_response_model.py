from typing import Any, List

from pydantic import BaseModel, Field, field_validator

from constants.roles import Roles

class UserModel(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: list[Roles]
    verified: bool
    createdAt: str
    banned: bool

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

class GetAllUsersResponseModel(BaseModel):
    users: list[UserModel]
    count: int
    page: int
    pageSize: int

    @field_validator("users")
    def from_object_to_dict(cls, value: list[UserModel]) -> list[dict[str, Any] | None]:
        new_list = []
        for user in value:
            new_list.append(vars(user))
        value = new_list
        return value

