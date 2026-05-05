# backend/models/location.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

location_contacts = Table(
    "location_contacts",
    Base.metadata,
    Column(
        "location_id",
        UUID(as_uuid=True),
        ForeignKey("locations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "contact_id",
        UUID(as_uuid=True),
        ForeignKey("contacts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Location(Base):
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas.id"), nullable=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=True, unique=True)
    description = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    floorplan = relationship(
        "LocationFloorplan", uselist=False, back_populates="location"
    )
    site = relationship("Site")
    area = relationship("Area", back_populates="locations")
    tenant = relationship("Tenant")
    assets = relationship("Asset", back_populates="location")
    contacts = relationship("Contact", secondary=location_contacts, backref="locations")


class LocationFloorplan(Base):
    __tablename__ = "location_floorplans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    location_id = Column(
        UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False, unique=True
    )
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=func.now())
    location = relationship("Location", back_populates="floorplan")
