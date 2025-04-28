from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from datetime import datetime

from .recipes_resources import RecipesResource
from ..dependencies.database import Base
from ..schemas.recipes import ResourceInRecipe
from ..schemas.resources import Resource as ResourceSchema


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    #menu_items = relationship("MenuItem", back_populates="recipes")
    resources_link = relationship("RecipesResource", back_populates="recipe", cascade="all, delete-orphan")

    @property
    def resources(self):
        return [
            {
                "resource": {
                    "id": link.resource.id,
                    "item": link.resource.item,
                    "amount": link.resource.amount,
                    "unit": link.resource.unit,
                    "status": link.resource.status,
                },
                "amount": link.amount
            }
            for link in self.resources_link
        ]

    #resources = association_proxy("resources_link", "resource",
    #                              creator = lambda resource_and_amount: RecipesResource(
    #                                  resource=resource_and_amount["resource"],
    #                                  amount=resource_and_amount["amount"])
    #                              )
    #recipes_resources = relationship("RecipesResource", back_populates="recipes")
    #categories = relationship("Category", back_populates="recipes")