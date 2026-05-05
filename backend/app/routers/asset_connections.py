# routers/asset_connections.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.errors.exceptions import ErrorCodeException
from app.errors.error_codes import ErrorCode
from app.services.audit_decorator import audit_log_action
from app.database import get_db
from app.services.auth import get_current_user
from app.models import User, AssetConnection
from app.schemas import (
    AssetConnection as AssetConnectionSchema,
    AssetConnectionCreate,
    AssetConnectionUpdate,
)
from app.crud import asset_connections as crud_assetconnections

router = APIRouter(
    prefix="/assets/{asset_id}/connections",
    tags=["assets"],
)


@router.get("", response_model=List[AssetConnectionSchema])
def list_connections(
    asset_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get connections where the asset is parent or child
    parent_connections = crud_assetconnections.get_asset_connections_by_parent(
        db, asset_id, current_user.tenant_id
    )
    child_connections = crud_assetconnections.get_asset_connections_by_child(
        db, asset_id, current_user.tenant_id
    )
    return parent_connections + child_connections


@router.post("", response_model=AssetConnectionSchema)
@audit_log_action("create", "AssetConnection", model_class=AssetConnection)
def create_connection(
    asset_id: uuid.UUID,
    request: Request,
    data: AssetConnectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Set the asset_id as parent_asset_id if not specified
    if not data.parent_asset_id:
        data.parent_asset_id = asset_id
    return crud_assetconnections.create_asset_connection(
        db, data, current_user.tenant_id
    )


@router.put("/{connection_id}", response_model=AssetConnectionSchema)
@audit_log_action("update", "AssetConnection", model_class=AssetConnection)
def update_connection(
    asset_id: uuid.UUID,
    connection_id: uuid.UUID,
    request: Request,
    data: AssetConnectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conn = crud_assetconnections.get_asset_connection(
        db, connection_id, current_user.tenant_id
    )
    if not conn:
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.ASSET_CONNECTION_NOT_FOUND
        )
    return crud_assetconnections.update_asset_connection(db, conn, data)


@router.delete("/{connection_id}")
@audit_log_action("delete", "AssetConnection", model_class=AssetConnection)
def delete_connection(
    asset_id: uuid.UUID,
    connection_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conn = crud_assetconnections.get_asset_connection(
        db, connection_id, current_user.tenant_id
    )
    if not conn:
        raise ErrorCodeException(
            status_code=404, error_code=ErrorCode.ASSET_CONNECTION_NOT_FOUND
        )
    crud_assetconnections.delete_asset_connection(db, conn)
    return {"detail": "Connection deleted"}
