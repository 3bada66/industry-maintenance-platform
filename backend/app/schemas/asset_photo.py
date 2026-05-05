# backend/schemas/asset_photo.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class AssetPhotoBase(BaseModel):
    asset_id: uuid.UUID
    file_path: str


class AssetPhotoCreate(AssetPhotoBase):
    tenant_id: uuid.UUID


class AssetPhoto(AssetPhotoBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    uploaded_at: Optional[datetime] = None

    class Config:
        from_attributes = True
