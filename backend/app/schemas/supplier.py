# backend/schemas/supplier.py

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import uuid
from app.schemas.validators import *


class SupplierBase(BaseModel):
    name: str = Field(..., max_length=255, description="Supplier name")
    description: Optional[str] = Field(None, max_length=10000, description="Supplier description")
    vat_number: Optional[str] = Field(None, max_length=50, description="VAT number")
    tax_code: Optional[str] = Field(None, max_length=50, description="Tax code")
    address: Optional[str] = Field(None, max_length=255, description="Address")
    city: Optional[str] = Field(None, max_length=100, description="City")
    zip_code: Optional[str] = Field(None, max_length=20, description="ZIP code")
    province: Optional[str] = Field(None, max_length=50, description="Province")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    email: Optional[str] = Field(None, max_length=255, description="Email address")
    website: Optional[str] = Field(None, max_length=255, description="Website URL")
    notes: Optional[str] = Field(None, max_length=10000, description="Notes")

    # Validators
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone)
    _validate_website = validator('website', allow_reuse=True)(validate_website)
    _validate_vat_number = validator('vat_number', allow_reuse=True)(validate_vat_number)
    _validate_tax_code = validator('tax_code', allow_reuse=True)(validate_tax_code)
    _validate_email = validator('email', allow_reuse=True)(validate_email)


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Supplier name")
    description: Optional[str] = Field(None, max_length=10000, description="Supplier description")
    vat_number: Optional[str] = Field(None, max_length=50, description="VAT number")
    tax_code: Optional[str] = Field(None, max_length=50, description="Tax code")
    address: Optional[str] = Field(None, max_length=255, description="Address")
    city: Optional[str] = Field(None, max_length=100, description="City")
    zip_code: Optional[str] = Field(None, max_length=20, description="ZIP code")
    province: Optional[str] = Field(None, max_length=50, description="Province")
    country: Optional[str] = Field(None, max_length=100, description="Country")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    email: Optional[str] = Field(None, max_length=255, description="Email address")
    website: Optional[str] = Field(None, max_length=255, description="Website URL")
    notes: Optional[str] = Field(None, max_length=10000, description="Notes")

    # Validators
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone)
    _validate_website = validator('website', allow_reuse=True)(validate_website)
    _validate_vat_number = validator('vat_number', allow_reuse=True)(validate_vat_number)
    _validate_tax_code = validator('tax_code', allow_reuse=True)(validate_tax_code)
    _validate_email = validator('email', allow_reuse=True)(validate_email)


class SupplierDocumentBase(BaseModel):
    filename: str
    filepath: str


class SupplierDocumentCreate(SupplierDocumentBase):
    tenant_id: uuid.UUID


class SupplierDocument(SupplierDocumentBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    uploaded_at: datetime

    class Config:
        from_attributes = True


class Supplier(SupplierBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    documents: List[SupplierDocument] = []

    class Config:
        from_attributes = True
