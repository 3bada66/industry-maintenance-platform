# backend/models/supplier.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

supplier_contacts = Table(
    "supplier_contacts",
    Base.metadata,
    Column(
        "supplier_id",
        UUID(as_uuid=True),
        ForeignKey("suppliers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "contact_id",
        UUID(as_uuid=True),
        ForeignKey("contacts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    contacts = relationship("Contact", secondary=supplier_contacts, backref="suppliers")
    documents = relationship(
        "SupplierDocument", back_populates="supplier", cascade="all, delete-orphan"
    )
    vat_number = Column(String(50), nullable=True)
    tax_code = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    province = Column(String(50), nullable=True)
    country = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    deleted_at = Column(DateTime, nullable=True)


class SupplierDocument(Base):
    __tablename__ = "supplier_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    supplier_id = Column(
        UUID(as_uuid=True),
        ForeignKey("suppliers.id", ondelete="CASCADE"),
        nullable=False,
    )
    filename = Column(String(255), nullable=False)
    filepath = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=func.now())
    supplier = relationship("Supplier", back_populates="documents")
