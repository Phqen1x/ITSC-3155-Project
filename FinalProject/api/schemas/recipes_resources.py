from typing import Optional
from pydantic import BaseModel


class RecipesResourceBase(BaseModel):
    amount: int

class RecipesResourceCreate(RecipesResourceBase):
    pass


class RecipesResourceUpdate(RecipesResourceBase):
    amount: Optional[int] = None


class RecipesResource(RecipesResourceBase):
    id: int

    class ConfigDict:
        from_attributes = True