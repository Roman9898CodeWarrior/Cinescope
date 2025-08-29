from typing import Any, List

from pydantic import BaseModel, Field, field_validator

class Payment(BaseModel):
    id: int
    userId: str
    movieId: int
    total: int
    amount: int
    createdAt: str
    status: str

class UserPaymentsResponse(BaseModel):
        payments: List[Payment]