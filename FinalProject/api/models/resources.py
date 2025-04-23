from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = Column(String(100), unique=True, nullable=False)
    amount = Column(Integer, index=True, nullable=False, server_default='0.0')
    unit = Column(String(100), unique=False, nullable=False)
    status = Column(String(100), unique=False, nullable=True)

    recipes = relationship("Recipe", back_populates="resources")
    recipes_resources = relationship("RecipesResource",
                                     back_populates="resources")

