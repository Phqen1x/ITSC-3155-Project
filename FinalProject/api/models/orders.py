from decimal import Decimal

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
    total_price = Column(DECIMAL(10, 2), nullable=False, unique=False)
    type = Column(String(100), nullable=False, unique=False)
    status = Column(String(100), nullable=False, unique=False)
    promotion_id = Column(Integer, ForeignKey("promotions.id"))

    # Order Statuses
    order_placed = Column(DATETIME, nullable=True)
    order_canceled = Column(DATETIME, nullable=True)
    order_prepping = Column(DATETIME, nullable=True)
    order_ready = Column(DATETIME, nullable=True)

    # Review Variables
    review_text = Column(String(500))
    review_rating = Column(DECIMAL)

    # Relationships
    order_details = relationship("OrderDetail", back_populates="order",
                                 cascade="all, delete-orphan")
    promotions = relationship("Promotion", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")

    def calculate_total_price(self, discount=None):
        total = Decimal(0)
        for detail in self.order_details:
            if detail.menu_item and detail.menu_item.price is not None:
                total += Decimal(detail.amount) * detail.menu_item.price
                print(total)
            else:
                raise ValueError(
                    f"Missing price or menu_item for item_id {detail.item_id}"
                )
        if discount:
            total *= Decimal((100-discount)/100)
        self.total_price = total
