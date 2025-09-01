from pydantic import BaseModel, Field, model_validator, field_validator

from constants.roles import Roles

class UserDataForRegistration(BaseModel):
    email: str
    fullName: str
    password: str = Field(min_length=8, max_length=32)
    passwordRepeat: str
    #roles: list[str] = [Roles.USER.value]
    roles: list[Roles] = [Roles.USER]

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if '@' not in value:
            raise ValueError("В имейле д.б. @.")
        return value

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

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

class UserDataForCreationByAdmin(BaseModel):
    email: str
    fullName: str
    password: str = Field(min_length=8, max_length=32)
    verified: bool
    banned: bool

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if '@' not in value:
            raise ValueError("В имейле д.б. @.")
        return value

class UserDataForLoggingIn(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=32)

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if '@' not in value:
            raise ValueError("В имейле д.б. @.")
        return value