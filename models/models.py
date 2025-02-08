from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class RequestModel(BaseModel):
    name: str
    phone: str
    email: EmailStr
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    postcode: str
    numPeople: int = Field(..., ge=1, le=10)
    ages: List[str]
    attending_date: str
    transport: str
    carPool: Optional[bool] = False
    carPoolSeats: Optional[int] = 0
    accommodation: str
    homeSpace: Optional[bool] = False
    homeSpaceCount: Optional[int] = 0
    totalFees: float
    paymentConfirmed: bool


class WithdrawalUpdate(BaseModel):
    status: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    userId: object
    username: str
    name: str
    email: str
    phone: str

class UserInDB(User):
    hashed_password: str





