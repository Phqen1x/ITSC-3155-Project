from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MenuItemBase(BaseModel):
    item_name: str
    price: float
    calories: int
    category: str


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    sandwich_name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None


class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True
