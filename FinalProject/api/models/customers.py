from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), unique=True, nullable=True)
    customer_email = Column(String(100), unique=True, nullable=True)
    customer_phone_number = Column(String(100), unique=True, nullable=True)
    customer_address = Column(String(100), unique=False, nullable=True)

    payment_information= relationship("PaymentInfo", back_populates="customers")
