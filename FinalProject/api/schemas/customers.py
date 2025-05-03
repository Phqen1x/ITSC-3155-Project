from typing import Optional
from pydantic import BaseModel



class CustomerBase(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone_number: str
    customer_address: str


class CustomerOrders(BaseModel):
    customer_name: str
    description: str
    total_price: float
    type: Optional[str] = "Dine-In"
    status: Optional[str] = "Your order is currently being processed."
    promotion_code: Optional[int] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone_number: Optional[str] = None
    customer_address: Optional[str] = None


class Customer(CustomerBase):
    id: int
    customer_email: str
    customer_phone_number: str
    customer_address: str

    class ConfigDict:
        from_attributes = True

