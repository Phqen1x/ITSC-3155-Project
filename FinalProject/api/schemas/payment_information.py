from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PaymentBase(BaseModel):
    card_number: str
    card_expir_date: datetime
    card_cvc: int

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    card_number: Optional[str] = None
    card_expir_date: Optional[datetime] = None
    card_cvc: Optional[int] = None

class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True

