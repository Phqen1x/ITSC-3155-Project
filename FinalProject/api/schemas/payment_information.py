from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail



class PaymentBase(BaseModel):
    customer_name: str
    order_total: float

class PaymentUpdate(BaseModel):
    customer_name: Optional[str] = None
    order_total: Optional[float] = None

class Order(OrderBase):
    id: int
    card_number: Optional[str] = None
    card_expir_date: Optional[datetime] = None
    card_cvc: Optional[int] = None

    class ConfigDict:
        from_attributes = True

