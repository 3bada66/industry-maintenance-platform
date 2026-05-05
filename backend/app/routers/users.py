import uuid
from typing import List

from fastapi import APIRouter, Depends, Request, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas.user import UserCreate, UserUpdate, UserRead, PasswordChange
from app.services.auth import get_current_user, get_password_hash
from app.services.audit_decorator import audit_log_action
from app.services.rbac import require_permission
from app.crud import users as crud_users
from app.errors.exceptions import ErrorCodeException
from app.errors.error_codes import ErrorCode
from sqlalchemy.exc import IntegrityError
import secrets

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("", response_model=UserRead)
@audit_log_action("create", "User", model_class=User)
def create_user(
    user: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            tenant_id=current_user.tenant_id,
            email=user.email,
            password_hash=hashed_password,
            name=user.name,
            role_id=user.role_id,
            is_active=user.is_active if user.is_active is not None else True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ErrorCodeException(
            status_code=400,
            error_code=ErrorCode.INVALID_USER_CREATION,
        )
    except Exception as e:
        db.rollback()
        raise ErrorCodeException(
            status_code=500,
            error_code=ErrorCode.INVALID_USER_CREATION,
        )


@router.delete("/{user_id}")
@audit_log_action("delete", "User", model_class=User)
def delete_user(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = crud_users.get_user(db, user_id, current_user.tenant_id)
    if not user:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.USER_NOT_FOUND)
    crud_users.delete_user(db, user)
    return None


@router.put("/{user_id}", response_model=UserRead)
@audit_log_action("update", "User", model_class=User)
def update_user(
    user_id: uuid.UUID,
    user: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_user = crud_users.get_user(db, user_id, current_user.tenant_id)
    if not db_user:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.USER_NOT_FOUND)
    return crud_users.update_user(db, db_user, user)


@router.get("/{user_id}", response_model=UserRead)
@audit_log_action("get", "User", model_class=User)
def get_user(
    user_id: uuid.UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = crud_users.get_user(db, user_id, current_user.tenant_id)
    if not user:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.USER_NOT_FOUND)
    return user


@router.get("", response_model=List[UserRead])
def list_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
):
    return crud_users.get_users(db, current_user.tenant_id, skip=skip, limit=limit)


@router.post("/{user_id}/reset-password")
@audit_log_action("reset_password", "User", model_class=User)
def reset_password(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    perm=Depends(require_permission("reset_user_password", 1)),
):
    user = (
        db.query(User)
        .filter(User.id == user_id, User.tenant_id == current_user.tenant_id)
        .first()
    )
    if not user:
        raise ErrorCodeException(status_code=404, error_code=ErrorCode.USER_NOT_FOUND)
    
    # Generate temporary password
    new_password = secrets.token_urlsafe(10)
    user.password_hash = get_password_hash(new_password)
    db.commit()
    
    # Return the temporary password to the admin
    return {
        "detail": "Password reset successfully",
        "temporary_password": new_password,
        "user_email": user.email
    }


@router.post("/reset-password")
def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Allow the user to change their password"""
    from app.services.auth import verify_password

    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise ErrorCodeException(
            status_code=400, error_code=ErrorCode.INVALID_CREDENTIALS
        )

    # Update password
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()

    return {"detail": "Password updated successfully"}
