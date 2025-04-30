from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer_name = Column(String(100), nullable=False, unique=False)
    description = Column(String(500), nullable=False, unique=False)
    total_price = Column(DECIMAL(4, 2), nullable=False, unique=False)
    type = Column(String(100), nullable=False, unique=False)
    status = Column(String(100), nullable=False, unique=False)

    # Order Statuses
    # order_placed = Column(DATETIME, server_default=str(datetime.now()))
    # order_prepping = Column(DATETIME, nullable=True)
    # order_ready = Column(DATETIME, nullable=True)

    # Review Variables
    review_text = Column(String(500))
    review_rating = Column(DECIMAL)

    promotion_code = Column(Integer, ForeignKey("promotions.id"))

    # Relationships
    order_details = relationship("OrderDetail", back_populates="orders")
    # menu_items = relationship("MenuItem", back_populates="orders")
    promotions = relationship("Promotion", back_populates="orders")
