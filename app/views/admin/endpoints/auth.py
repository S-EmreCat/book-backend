from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import auth_core
from app.core.panel_user import panel_user_core
from app.helpers.error_helper import Error
from app.helpers.hash_helper import hash_helper
from app.schemas.admin.auth import AdminLoginIn, AdminLoginOut
from app.views.deps import get_db

router = APIRouter()


@router.post("/login", response_model=AdminLoginOut, summary="Giriş Yap")
def login(
    data: AdminLoginIn,
    db: Session = Depends(get_db),
):
    panel_user = panel_user_core.get_panel_user_by_email(db=db, email=data.email)
    if not panel_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_login)

    if not hash_helper.verify(panel_user.password_hash, data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_login)

    return auth_core.panel_user_login(panel_user=panel_user)
