from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promotion_code = Column(String(100), unique=True, nullable=True)
    expiration_date = Column(String(100), nullable=True, unique=False)
    discount = Column(Integer, index=True, nullable=True, server_default='0.0') 

    menu_items = relationship("MenuItem", back_populates="promotion")
