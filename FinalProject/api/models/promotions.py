from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Boolean
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promotion_code = Column(String(100), unique=True)
    expiration_date = Column(DATETIME, nullable=True, unique=False)
    discount = Column(Integer, nullable=True, server_default='0.0') 
    active = Column(Boolean, server_default=expression.true())

    # menu_items = relationship("MenuItem", back_populates="promotions")
    orders = relationship("Order", back_populates="promotions")
