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
