# routers/tenants.py

from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services.auth import get_current_user
from app.services.audit_decorator import audit_log_action
from app.models import Tenant
from app.crud import tenants as crud_tenants

router = APIRouter(
    prefix="/tenants",
    tags=["tenants"],
)


@router.post("", response_model=schemas.Tenant)
@audit_log_action("create", "Tenant", model_class=Tenant)
def create_tenant(
    tenant: schemas.Tenant,
    request: Request,
    db: Session = Depends(get_db),
    current_user: object = Depends(get_current_user),
):
    if not current_user.role or current_user.role.name.lower() != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin role required")
    return crud_tenants.create_tenant(db, tenant)


@router.get("", response_model=List[schemas.Tenant])
@audit_log_action("list", "Tenant", model_class=Tenant)
def list_tenants(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: object = Depends(get_current_user),
):
    if not current_user.role or current_user.role.name.lower() != "admin":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin role required")
    return crud_tenants.get_tenants(db, skip=skip, limit=limit)
