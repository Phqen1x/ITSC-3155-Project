from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class PaymentInfo(Base):
    __tablename__ = "payment_information"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_number = Column(String(100), unique=True, nullable=False)
    card_expir_date = Column(DATETIME, unique=False, nullable=False)
    card_cvc = Column(Integer, unique=False, nullable=False
    transaction_status = Column(String(100), unique=False, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    customers = relationship("Customer", back_populates="payment_information")
