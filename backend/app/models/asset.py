# backend/models/asset.py
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    ForeignKey,
    Float,
    Table,
    Integer,
    Boolean,
    Date,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database import Base
from app.models.asset_status import AssetStatus
from app.models.contact import Contact
from app.models.asset_communication import AssetCommunication

asset_contacts = Table(
    "asset_contacts",
    Base.metadata,
    Column(
        "asset_id",
        UUID(as_uuid=True),
        ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "contact_id",
        UUID(as_uuid=True),
        ForeignKey("contacts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

asset_suppliers = Table(
    "asset_suppliers",
    Base.metadata,
    Column(
        "asset_id",
        UUID(as_uuid=True),
        ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "supplier_id",
        UUID(as_uuid=True),
        ForeignKey("suppliers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    asset_type_id = Column(
        UUID(as_uuid=True), ForeignKey("asset_types.id"), nullable=False
    )
    status_id = Column(
        UUID(as_uuid=True), ForeignKey("asset_statuses.id"), nullable=False
    )
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas.id"), nullable=True)
    manufacturer_id = Column(
        UUID(as_uuid=True), ForeignKey("manufacturers.id"), nullable=True, index=True
    )
    name = Column(String(255), nullable=False)
    tag = Column(String(100))
    serial_number = Column(String(100))
    model = Column(String(100))
    firmware_version = Column(String(50))
    remote_access = Column(Boolean, default=False)  # Accesso remoto abilitato
    remote_access_type = Column(
        String(20), default="none"
    )  # 'none', 'attended', 'unattended'
    last_update_date = Column(DateTime, nullable=True)
    description = Column(Text)
    custom_fields = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_seen = Column(DateTime)
    map_x = Column(Float, nullable=True)
    map_y = Column(Float, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    installation_date = Column(Date, nullable=True)
    business_criticality = Column(String, nullable=True)
    protocols = Column(JSONB, default=list)
    impact_value = Column(Integer, default=1)  # 1-5 scale
    physical_access_ease = Column(
        String(50), default="internal"
    )  # internal/dmz/external
    purdue_level = Column(Float, default=0.0)  # 0.0-5.0
    exposure_level = Column(String(50), default="none")  # none/low/medium/high
    update_status = Column(String(50), default="manual")  # manual/imported/auto
    risk_score = Column(Float, default=0.0)  # calculated field 0-100
    last_risk_assessment = Column(DateTime, default=func.now())
    status = relationship("AssetStatus", back_populates="assets")
    site = relationship("Site", back_populates="assets")
    asset_type = relationship("AssetType", back_populates="assets")
    photos = relationship("AssetPhoto", back_populates="asset", cascade="all, delete")
    documents = relationship(
        "AssetDocument", back_populates="asset", cascade="all, delete"
    )
    manufacturer = relationship("Manufacturer", back_populates="assets")
    contacts = relationship("Contact", secondary=asset_contacts, backref="assets")
    suppliers = relationship("Supplier", secondary=asset_suppliers, backref="assets")
    location = relationship("Location", back_populates="assets")
    area = relationship("Area", back_populates="assets")
    interfaces = relationship(
        "AssetInterface", back_populates="asset", cascade="all, delete-orphan"
    )
