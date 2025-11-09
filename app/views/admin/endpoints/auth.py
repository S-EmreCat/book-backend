from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.auth import auth_core
from app.core.panel_user import panel_user_core
from app.helpers.error_helper import Error
from app.helpers.hash_helper import hash_helper
from app.models.panel_user_login_history import PanelUserLoginHistory
from app.schemas.admin.auth import LoginIn, LoginOut
from app.views.deps import get_db

router = APIRouter()


@router.post("/login", response_model=LoginOut, summary="Giriş Yap")
def login(
    data: LoginIn,
    request: Request,
    db: Session = Depends(get_db),
):
    panel_user = panel_user_core.get_panel_user_by_email(db=db, email=data.email)
    if not panel_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_login)

    if not hash_helper.verify(panel_user.password_hash, data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_login)

    # Login başarılıysa token oluştur
    login_result = auth_core.panel_user_login(panel_user=panel_user)

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    login_history = PanelUserLoginHistory(
        panel_user_id=panel_user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(login_history)
    db.commit()

    return login_result
