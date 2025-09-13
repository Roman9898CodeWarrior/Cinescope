import datetime

from pydantic import BaseModel, Field, field_validator

from constants.roles import Roles


class RegisterCreateGetOrDeleteUserResponseModel(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: list[Roles]
    verified: bool
    createdAt: str
    #banned: bool

    class Config:
        json_encoders = {
            Roles: lambda v: v.value
        }

    @field_validator("roles")
    def from_enum_to_str(cls, value: list[Roles]) -> list[str]:
        new_list = []
        for role in value:
            new_list.append(role.value)
        value = new_list
        return value

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value


class ChangeUserResponseModel(BaseModel):
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: list[Roles]
    verified: bool
    createdAt: str
    #banned: bool

    class Config:
        json_encoders = {
            Roles: lambda v: v.value
        }

    @field_validator("roles")
    def from_enum_to_str(cls, value: list[Roles]) -> list[str]:
        new_list = []
        for role in value:
            new_list.append(role.value)
        value = new_list
        return value

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value
