# backend/crud/manufacturers.py
from sqlalchemy.orm import Session
from app.models import Manufacturer
from app.schemas import ManufacturerCreate, ManufacturerUpdate
import uuid
from typing import List, Optional
from datetime import datetime, timezone
from app.errors.error_codes import ErrorCode
from app.errors.exceptions import ErrorCodeException
from app.utils import sanitize_text_fields


def create_manufacturer(
    db: Session, manufacturer_in: ManufacturerCreate, tenant_id: uuid.UUID
) -> Manufacturer:
    """Create a new manufacturer"""
    data = sanitize_text_fields(
        manufacturer_in.dict(exclude={"tenant_id"}), ["description", "notes"]
    )
    data["tenant_id"] = tenant_id
    manufacturer = Manufacturer(**data)
    db.add(manufacturer)
    db.commit()
    db.refresh(manufacturer)
    return manufacturer


def list_manufacturers(db: Session, tenant_id: uuid.UUID) -> List[Manufacturer]:
    """List all manufacturers of a tenant"""
    return db.query(Manufacturer).filter(Manufacturer.tenant_id == tenant_id).all()


def get_manufacturer(
    db: Session, manufacturer_id: uuid.UUID, tenant_id: uuid.UUID
) -> Optional[Manufacturer]:
    """Retrieve a manufacturer by ID"""
    return (
        db.query(Manufacturer)
        .filter(Manufacturer.id == manufacturer_id, Manufacturer.tenant_id == tenant_id)
        .first()
    )


def update_manufacturer(
    db: Session, manufacturer, update_data: ManufacturerUpdate
) -> Manufacturer:
    """Update an existing manufacturer"""
    update_data_dict = sanitize_text_fields(
        update_data.dict(exclude_unset=True), ["description", "notes"]
    )
    for key, value in update_data_dict.items():
        setattr(manufacturer, key, value)
    manufacturer.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(manufacturer)
    return manufacturer


def delete_manufacturer(db: Session, manufacturer):
    """Delete a manufacturer"""
    if manufacturer.assets and len(manufacturer.assets) > 0:
        raise ErrorCodeException(
            status_code=400, error_code=ErrorCode.MANUFACTURER_LINKED_TO_ASSETS
        )
    db.delete(manufacturer)
    db.commit()
