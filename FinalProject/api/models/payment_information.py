from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class PaymentInfo(Base):
    __tablename__ = "payment_information"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_info = Column(String(100), unique=True, nullable=False)
    transaction_status = Column(String(100), unique=False, nullable=False)
    payment_type = Columb(String(100), unique=False, nullable=F]alse)

    customers = relationship("Customer", back_populates="payment_information")
