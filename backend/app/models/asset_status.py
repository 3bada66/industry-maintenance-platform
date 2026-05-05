import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class AssetStatus(Base):
    __tablename__ = "asset_statuses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    color = Column(String(7), default="#64748b")
    active = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    assets = relationship("Asset", back_populates="status")
