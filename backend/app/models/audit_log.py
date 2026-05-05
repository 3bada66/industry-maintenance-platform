# backend/models/audit_log.py

import uuid
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(
        String(50), nullable=False
    )  
    entity = Column(
        String(100), nullable=False
    )  
    entity_id = Column(UUID(as_uuid=True), nullable=True)  
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45), nullable=True)  
    old_data = Column(JSON, nullable=True)  
    new_data = Column(JSON, nullable=True)  
    description = Column(
        String(255), nullable=True
    )  
