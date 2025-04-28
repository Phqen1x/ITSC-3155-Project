from typing import Optional
from pydantic import BaseModel


class CategoryBase(BaseModel):
    type: str

class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    type: str


class Category(CategoryBase):
    id: int

    class ConfigDict:
        from_attributes = True
