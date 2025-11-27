from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import SessionLocal
from app.models.user import User


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")
        return {"id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token.")


def require_role(*allowed_roles):
    def wrapper(token: str = Depends(get_current_user)):
        if token["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission."
            )
        return token
    return wrapper
