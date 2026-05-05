from fastapi import Depends, HTTPException, status
from app.services.auth import get_current_user
from app.models import User


def require_permission(section: str, min_level: int):
    """
    Dependency FastAPI per RBAC basato su ruolo.
    section: nome della sezione (es: 'assets', 'sites', ...)
    min_level: livello minimo richiesto (0=none, 1=read, 2=write, 3=delete)
    """

    def dependency(current_user: User = Depends(get_current_user)):
        role = getattr(current_user, "role", None)
        if not role or not role.permissions:
            user_level = 0
        else:
            user_level = role.permissions.get(section, 0)
        if user_level < min_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied for {section} (required: {min_level}, user: {user_level})",
            )
        return True

    return dependency
