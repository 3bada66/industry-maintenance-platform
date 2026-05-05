import uuid
from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TenantSMTPConfig, Tenant, User
from app.schemas.tenant_smtp_config import (
    TenantSMTPConfigRead,
    TenantSMTPConfigCreate,
    TenantSMTPConfigUpdate,
)
from app.services.auth import get_current_user
from app.services.email_service import EmailConfig, EmailProvider, send_email
from app.errors.exceptions import ErrorCodeException
from app.errors.error_codes import ErrorCode
from pydantic import EmailStr

router = APIRouter(
    prefix="/smtp-config",
    tags=["smtp-config"],
)


@router.get("", response_model=TenantSMTPConfigRead)
def get_smtp_config(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    config = (
        db.query(TenantSMTPConfig)
        .filter(TenantSMTPConfig.tenant_id == current_user.tenant_id)
        .first()
    )
    if not config:
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.SMTP_CONFIG_NOT_FOUND
        )
    return config


@router.post("", response_model=TenantSMTPConfigRead)
def set_smtp_config(
    config_in: TenantSMTPConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = (
        db.query(TenantSMTPConfig)
        .filter(TenantSMTPConfig.tenant_id == current_user.tenant_id)
        .first()
    )
    if config:
        for field, value in config_in.dict().items():
            setattr(config, field, value)
    else:
        config = TenantSMTPConfig(**config_in.dict(), tenant_id=current_user.tenant_id)
        db.add(config)
    db.commit()
    db.refresh(config)
    return config


@router.post("/test")
def test_smtp_config(
    to_email: EmailStr,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    config = (
        db.query(TenantSMTPConfig)
        .filter(TenantSMTPConfig.tenant_id == current_user.tenant_id)
        .first()
    )
    if not config:
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.SMTP_CONFIG_NOT_FOUND
        )
    
    # Converti configurazione database in EmailConfig
    email_config = EmailConfig(
        provider=EmailProvider(config.provider or "smtp"),
        api_key=config.api_key,
        domain=config.domain,
        region=config.region,
        from_email=config.from_email,
        credentials=config.credentials,
        smtp_host=config.host,
        smtp_port=config.port,
        smtp_username=config.username,
        smtp_password=config.password,
        smtp_use_tls=config.use_tls
    )
    
    try:
        success = send_email(to_email, "Test Email", "This is a test email from Industry Maintenance Platform.", email_config)
        if success:
            return {"detail": "Test email sent successfully"}
        else:
            raise ErrorCodeException(status_code=400, error_code=ErrorCode.SMTP_SEND_ERROR)
    except Exception as e:
        raise ErrorCodeException(status_code=400, error_code=ErrorCode.SMTP_SEND_ERROR)
