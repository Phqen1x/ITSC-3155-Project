#An intermediary table for many-to-many relationship between resources and recipes
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, false
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from ..dependencies.database import Base

class RecipesCategories(Base):
    __tablename__ = "recipes_categories"

    #id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True,
                       autoincrement=False)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True,
                         autoincrement=False)

    recipe = relationship("Recipe", back_populates="categories_link")
    category = relationship("Category", back_populates="recipes")

    resource_item = association_proxy(target_collection='resource', attr='item')
    resource_amount = association_proxy(target_collection='resource', attr='amount')
    resource_unit = association_proxy(target_collection='resource', attr='unit')
    resource_status = association_proxy(target_collection='resource', attr='status')