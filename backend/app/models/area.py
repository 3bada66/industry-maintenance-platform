from sqlalchemy import Column, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class Area(Base):
    __tablename__ = "areas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    typology = Column(String(100), nullable=True)  # tipologia dell'area
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    tenant = relationship("Tenant", back_populates="areas")
    site = relationship("Site", back_populates="areas")
    locations = relationship("Location", back_populates="area")
    assets = relationship("Asset", back_populates="area")

    def __repr__(self):
        return f"<Area(id={self.id}, name='{self.name}', code='{self.code}')>" 