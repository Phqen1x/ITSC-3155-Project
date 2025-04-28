from typing import List

from pydantic import BaseModel, field_serializer

from ..schemas.resources import Resource


class RecipeBase(BaseModel):
    pass


class ResourceInRecipe(RecipeBase):
    resource: Resource
    amount: float

    class ConfigDict:
        from_attributes = True


class RecipeCreate(RecipeBase):
    resources: list[ResourceInRecipe]


class RecipeUpdate(BaseModel):
    resources: list[ResourceInRecipe]
    pass

class Recipe(RecipeBase):
    id: int
    resources: list[ResourceInRecipe]

    class ConfigDict:
        from_attributes = True