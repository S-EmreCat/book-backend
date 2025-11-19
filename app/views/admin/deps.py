from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.admin_user import admin_user_core
from app.helpers.secret_helper import secret_helper
from app.views.deps import get_db

oauth2_scheme = HTTPBearer()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_admin_user(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    payload = secret_helper.verify_token(token=token.credentials)
    admin_user = admin_user_core.get_admin_user_by_email(db=db, email=payload.get("email"))
    if not admin_user:
        raise credentials_exception
    return admin_user
