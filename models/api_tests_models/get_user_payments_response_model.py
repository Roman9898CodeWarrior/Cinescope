from pydantic import BaseModel, RootModel, field_validator

class PaymentModel(BaseModel):
    id: int
    userId: str
    movieId: int
    total: int
    amount: int
    createdAt: str
    status: str

class UserPaymentsResponseModel(RootModel[list[PaymentModel]]): ...


