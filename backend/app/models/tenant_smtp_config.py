import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class TenantSMTPConfig(Base):
    __tablename__ = "tenant_smtp_config"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, unique=True
    )
    
    # Provider moderno
    provider = Column(String, default="smtp")  # sendgrid, mailgun, aws_ses, gmail_oauth2, office365_oauth2, smtp
    api_key = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    region = Column(String, nullable=True)
    credentials = Column(JSON, nullable=True)  # Per OAuth2
    
    # SMTP fallback
    host = Column(String, nullable=True)
    port = Column(Integer, nullable=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)  
    from_email = Column(String, nullable=False)
    use_tls = Column(Boolean, default=True)
    
    tenant = relationship("Tenant", back_populates="smtp_config")
