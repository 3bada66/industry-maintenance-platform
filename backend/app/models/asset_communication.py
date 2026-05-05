# backend/models/asset_communication.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base   

class AssetCommunication(Base):
    __tablename__ = "asset_communications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    src_interface_id = Column(
        UUID(as_uuid=True), ForeignKey("asset_interfaces.id"), nullable=False
    )
    dst_interface_id = Column(
        UUID(as_uuid=True), ForeignKey("asset_interfaces.id"), nullable=False
    )
    packet_count = Column(Integer, default=0)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    site_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    src_interface = relationship("AssetInterface", foreign_keys=[src_interface_id])
    dst_interface = relationship("AssetInterface", foreign_keys=[dst_interface_id])
