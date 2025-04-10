from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource
from .MenuItem import MenuItem


class RecipeBase(BaseModel):
    amount: int


class RecipeCreate(RecipeBase):
    item_id: int
    resource_id: int

class RecipeUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    sandwich: MenuItem = None
    resource: Resource = None

    class ConfigDict:
        from_attributes = True