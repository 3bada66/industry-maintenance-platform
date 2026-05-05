from pydantic import BaseModel
from typing import Optional
import uuid


class AssetStatusBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = "#64748b"
    active: Optional[bool] = True
    order: Optional[int] = 0


class AssetStatusCreate(AssetStatusBase):
    tenant_id: Optional[uuid.UUID] = None


class AssetStatusUpdate(AssetStatusBase):
    pass


class AssetStatus(AssetStatusBase):
    id: uuid.UUID
    tenant_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True
