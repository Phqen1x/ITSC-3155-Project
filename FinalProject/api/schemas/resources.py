from typing import Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    item: str
    amount: int
    unit: str
    status: Optional[str] = None

class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(ResourceBase):
    item: Optional[str] = None
    amount: Optional[int] = None
    unit: Optional[str] = None
    status: Optional[str] = None


class Resource(ResourceBase):
    id: int
    status: Optional[str] = None

    class ConfigDict:
        from_attributes = True
