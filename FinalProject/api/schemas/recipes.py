from typing import List

from pydantic import BaseModel, field_serializer

from ..schemas.resources import Resource
from ..schemas.categories import Category

class RecipeBase(BaseModel):
    pass


class ResourceInRecipe(RecipeBase):
    resource: Resource
    amount: float

    class ConfigDict:
        from_attributes = True


class CategoryInRecipe(RecipeBase):
    category: Category

    class ConfigDict:
        from_attributes = True


class RecipeCreate(RecipeBase):
    resources: list[ResourceInRecipe]
    categories: list[CategoryInRecipe]


class RecipeUpdate(BaseModel):
    resources: list[ResourceInRecipe]
    pass

class Recipe(RecipeBase):
    id: int
    resources: list[ResourceInRecipe]

    class ConfigDict:
        from_attributes = True