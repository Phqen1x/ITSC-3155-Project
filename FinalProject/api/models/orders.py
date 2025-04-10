from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    tracking_number = Column(String(255), nullable=False)
    total_price = Column(DECIMAL, nullable=False)
    order_placed = Column(DATETIME, server_default=str(datetime.now()))
    order_prepping = Column(DATETIME, server_default="N/A")
    order_ready = Column(DATETIME, server_default="N/A")
    review_text = Column(String(500))
    review_rating = Column(DECIMAL)
