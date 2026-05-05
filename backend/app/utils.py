"""
Common utilities for the application
"""

import uuid
from typing import Any, Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import bleach


def generate_uuid() -> uuid.UUID:
    """Generate a UUID v4"""
    return uuid.uuid4()


def get_current_timestamp() -> datetime:
    """Get the current timestamp in UTC"""
    return datetime.now(timezone.utc)


def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values and private fields from a dictionary"""
    if not data:
        return {}

    result = {}
    for key, value in data.items():
        if key.startswith("_"):
            continue
        if value is not None:
            result[key] = value
    return result


def sanitize_text_fields(data: dict, fields: list) -> dict:
    """
    Apply bleach.clean to the specified fields of a dictionary.
    Return a new dictionary with the sanitized fields.
    """
    sanitized = data.copy()
    for field in fields:
        if field in sanitized and isinstance(sanitized[field], str):
            sanitized[field] = bleach.clean(sanitized[field])
    return sanitized


def build_tenant_filter(model_class, tenant_id: uuid.UUID):
    """Build a filter for tenant"""
    return model_class.tenant_id == tenant_id


def build_soft_delete_filter(model_class, include_deleted: bool = False):
    """Build a filter for soft delete"""
    if include_deleted:
        return None
    return model_class.deleted_at == None


def apply_pagination(query, skip: int = 0, limit: int = 100):
    """Apply pagination to a query"""
    return query.offset(skip).limit(limit)


def validate_uuid(uuid_string: str) -> Optional[uuid.UUID]:
    """Validate and convert a string to UUID"""
    try:
        return uuid.UUID(uuid_string)
    except (ValueError, AttributeError):
        return None


def format_datetime(dt: datetime) -> str:
    """Format a datetime to ISO string"""
    if dt is None:
        return None
    return dt.isoformat()


def parse_datetime(dt_string: str) -> Optional[datetime]:
    """Convert an ISO string to datetime"""
    try:
        return datetime.fromisoformat(dt_string.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
