from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .promotions import Promotion



class PromotionBase(BaseModel):
    code: str
    expir_date: datetime
    discount: int


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    code: Optional[str] = None
    expir_date: Optional[datetime] = None
    discount: Optional[int] = None


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True

