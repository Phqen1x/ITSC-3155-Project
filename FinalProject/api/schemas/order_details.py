from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .MenuItem import MenuItem


class OrderDetailBase(BaseModel):
    amount: int


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    item_id: int


class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    item_id: Optional[int] = None
    amount: Optional[int] = None


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    item: MenuItem = None

    class ConfigDict:
        from_attributes = True
