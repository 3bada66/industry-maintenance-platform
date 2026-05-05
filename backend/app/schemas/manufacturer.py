# backend/schemas/manufacturer.py

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import uuid
from app.schemas.validators import *


class ManufacturerBase(BaseModel):
    name: str = Field(..., max_length=255, description="Manufacturer name")
    description: Optional[str] = Field(None, max_length=10000, description="Manufacturer description")
    website: Optional[str] = Field(None, max_length=255, description="Website URL")
    email: Optional[str] = Field(None, max_length=255, description="Email address")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")

    # Validators
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone)
    _validate_website = validator('website', allow_reuse=True)(validate_website)
    _validate_email = validator('email', allow_reuse=True)(validate_email)


class ManufacturerCreate(ManufacturerBase):
    pass


class ManufacturerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    # Validators
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone)
    _validate_website = validator('website', allow_reuse=True)(validate_website)
    _validate_email = validator('email', allow_reuse=True)(validate_email)


class Manufacturer(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    description: Optional[str]
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
