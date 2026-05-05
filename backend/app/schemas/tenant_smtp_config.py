from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class TenantSMTPConfigBase(BaseModel):
    host: str
    port: int
    username: str
    password: str
    from_email: EmailStr
    use_tls: bool = True


class TenantSMTPConfigCreate(TenantSMTPConfigBase):
    pass


class TenantSMTPConfigUpdate(TenantSMTPConfigBase):
    pass


class TenantSMTPConfigRead(TenantSMTPConfigBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True
