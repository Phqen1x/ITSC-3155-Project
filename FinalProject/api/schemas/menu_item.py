
from typing import Optional
from pydantic import BaseModel

from .categories import Category


class MenuItemBase(BaseModel):
    item_name: str
    price: float
    calories: int
    category: str


class MenuItemCreate(MenuItemBase):
    recipe: int


class MenuItemUpdate(MenuItemBase):
    item_name: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None
    recipe_id: Optional[int] = None


class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True


class CategoryInMenu(BaseModel):
    category: Category

    class ConfigDict:
        from_attributes = True


class MenuItemCategory(BaseModel):
    categories: list[CategoryInMenu]
    #True = find if all categories match, false to find if ANY category matches
    search_and: bool = False

    class ConfigDict:
        from_attributes = True