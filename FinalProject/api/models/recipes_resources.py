#An intermediary table for many-to-many relationship between resources and recipes
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, false
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class RecipesResource(Base):
    __tablename__ = "recipes_resources"

    recipe_id = Column(Integer, ForeignKey("recipes.id"),
                       primary_key=True, autoincrement=False)
    resource_id = Column(Integer, ForeignKey("resources.id"),
                         primary_key=True, autoincrement=False)
    amount = Column(DECIMAL, default=0)

    recipes = relationship("Recipe", back_populates="recipes_resources")
    resource = relationship("Resource", back_populates="recipes_resources")