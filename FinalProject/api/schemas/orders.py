from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_name: str
    description: str
    total_price: float
    type: Optional[str] = "Dine-In"
    status: Optional[str] = "Your order is currently being processed."
    promotion_code: Optional[int] = None



class OrderCreate(OrderBase):
    pass


class OrderUpdateCustomer(OrderBase):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = "Dine-In"
    review_text: Optional[str] = None
    review_rating: Optional[float] = None


class OrderUpdateRestaurant(OrderBase):
    type: Optional[str] = "Dine-In"
    status: Optional[str] = "Your order is currently being process."


class OrderStatusUpdate(OrderBase):
    time: datetime

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
