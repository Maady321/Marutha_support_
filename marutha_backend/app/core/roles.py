# app/core/roles.py
from fastapi import HTTPException, status, Depends
from app.core.deps import get_current_user

def require_role(*allowed_roles):
    def role_dependency(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_dependency
