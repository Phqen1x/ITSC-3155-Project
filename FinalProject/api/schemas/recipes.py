from pydantic import BaseModel

from ..schemas.resources import Resource


class RecipeBase(BaseModel):
    pass


class ResourceInRecipe(RecipeBase):
    resource: Resource
    amount: float


class RecipeCreate(RecipeBase):
    resources: list[ResourceInRecipe]


class RecipeUpdate(BaseModel):
    pass

class Recipe(RecipeBase):
    id: int
    resources: list[Resource]

    class ConfigDict:
        from_attributes = True