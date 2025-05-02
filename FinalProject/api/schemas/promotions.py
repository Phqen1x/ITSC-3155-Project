from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PromotionBase(BaseModel):
    promotion_code: str
    expiration_date: datetime
    discount: int
    active: bool


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    promotion_code: Optional[str] = None
    expiration_date: Optional[datetime] = None
    discount: Optional[int] = None
    active: Optional[bool] = True


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True

