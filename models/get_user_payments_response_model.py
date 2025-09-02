from pydantic import BaseModel, RootModel, field_validator

class Payment(BaseModel):
    id: int
    userId: str
    movieId: int
    total: int
    amount: int
    createdAt: str
    status: str

class UserPaymentsResponse(RootModel[list[Payment]]): ...


