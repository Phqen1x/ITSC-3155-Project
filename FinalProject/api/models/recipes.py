from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from datetime import datetime

from .recipes_resources import RecipesResource
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    #item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    #resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)

    #menu_items = relationship("MenuItem", back_populates="recipes")
    resources_link = relationship("RecipesResource", back_populates="recipe")
    resources = association_proxy("resources_link", "resource",
                                  creator = lambda resource_and_amount: RecipesResource(
                                      resource=resource_and_amount["resource"],
                                      amount=resource_and_amount["amount"])
                                  )
    #recipes_resources = relationship("RecipesResource", back_populates="recipes")
    #categories = relationship("Category", back_populates="recipes")