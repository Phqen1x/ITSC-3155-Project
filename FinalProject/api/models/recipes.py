from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("menu_items.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    amount = Column(Integer, index=True, nullable=False, server_default='0.0')

    menu_items = relationship("MenuItem", back_populates="recipes")
    resources = relationship("Resource", back_populates="recipes")
    recipes_resources = relationship("RecipesResource", back_populates="recipes")
    categories = relationship("Category", back_populates="recipes")