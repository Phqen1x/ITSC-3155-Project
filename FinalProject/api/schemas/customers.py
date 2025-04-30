from typing import Optional
from pydantic import BaseModel



class CustomerBase(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone_number: str
    customer_address: str


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

