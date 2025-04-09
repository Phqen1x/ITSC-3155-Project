from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .payment_information import PaymentInfo

class PaymentBase(BaseModel):
    customer_name: str
    card_number: str
    card_expir_date: datetime
    card_cvc: int

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    customer_name: Optional[str] = None
    card_number: Optional[str] = None
    card_expir_date: Optional[datetime] = None
    card_cvc: Optional[int] = None

class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True

