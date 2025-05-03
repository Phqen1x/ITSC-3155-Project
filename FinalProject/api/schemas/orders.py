from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from .menu_item import MenuItem
from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_name: str
    description: str
    total_price: float
    type: Optional[str] = "Dine-In"
    #status: Optional[str] = "Your order is currently being processed."
    promotion_code: Optional[str] = None


class ItemsInOrder(BaseModel):
    item: MenuItem
    amount: float

    class ConfigDict:
        from_attributes = True


class OrderStatus(BaseModel):
    status: str
    time: float


class OrderCreate(OrderBase):
    items: list[ItemsInOrder]


class OrderUpdateCustomer(OrderBase):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = "Dine-In"
    # review_text: Optional[str] = None
    # review_rating: Optional[float] = None
    items: list[ItemsInOrder]


class OrderReview(BaseModel):
    review_text: Optional[str] = None
    review_rating: Optional[int] = None

class OrderUpdateRestaurant(OrderBase):
    type: Optional[str] = "Dine-In"
    items: list[ItemsInOrder]


class OrderStatusUpdate(OrderBase):
    time: datetime

class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
