from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

from .recipes_categories import RecipesCategories


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String(100), unique=True, nullable=False)

    recipes = relationship("RecipesCategories", back_populates="category")