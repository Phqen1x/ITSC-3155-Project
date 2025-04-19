from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String(100), unique=True, nullable=True)
    price = Column(DECIMAL(4, 2), nullable=False, server_default='0.0')
    calories = Column(Integer, nullable=False, server_default='0')
    category = Column(String(100), nullable=False, server_default='')

    recipes = relationship("Recipe", back_populates="menu_item")
    order_details = relationship("OrderDetail", back_populates="menu_item")
    promotion = relationship("Promotion", back_populates="menu_item")