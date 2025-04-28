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
    categories_link = relationship("RecipesCategories", back_populates="recipe", cascade="all, delete-orphan")

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

    @property
    def categories(self):
        return [
            {
                "category": {
                    "id": link.category.id,
                    "type": link.category.type,
                }
            }
            for link in self.categories_link
        ]