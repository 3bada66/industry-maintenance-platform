from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class PrintHistory(Base):
    __tablename__ = "print_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("print_templates.id"), nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String(500))
    file_size = Column(BigInteger)
    status = Column(String(50), default="completed")
    options = Column(JSON, default={})
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
