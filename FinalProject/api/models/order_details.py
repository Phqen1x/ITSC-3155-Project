from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class OrderDetail(Base):
    __tablename__ = "order_details"
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True,
                       autoincrement=False)
    item_id = Column(Integer, ForeignKey("menu_items.id"), primary_key=True,
                       autoincrement=False)
    amount = Column(Integer, index=True, nullable=False)

    menu_items = relationship("MenuItem", back_populates="order_details")
    orders = relationship("Order", back_populates="order_details")
