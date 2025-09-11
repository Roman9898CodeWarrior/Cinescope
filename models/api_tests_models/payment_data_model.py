from typing import Any

from pydantic import BaseModel, Field, field_validator

class CardModel(BaseModel):
        cardNumber: str = Field(min_length=16, max_length=16)
        cardHolder: str
        expirationDate: str = Field(min_length=5, max_length=5)
        securityCode: int

        @field_validator('securityCode')
        def check_security_cod(cls, value: int) -> int:
            if value < 0 or value > 999:
                raise ValueError("Код безопасности д.б. не меньше 0, но не больше 999")
            return value

class DataForPaymentCreationModel(BaseModel):
    movieId: int
    amount: int
    card: CardModel

    @field_validator("movieId")
    def check_movie_id(cls, value: int) -> int:
        if value < 1:
            raise ValueError("ID д.б. не меньше 1.")
        return value

    @field_validator("amount")
    def check_amount(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Количество билетов д.б. не меньше 1.")
        return value

    @field_validator("card")
    def from_object_to_dict(cls, value: CardModel) -> dict[str, Any] | None:
            return vars(value)

