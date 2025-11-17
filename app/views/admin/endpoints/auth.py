from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.auth import auth_core
from app.core.panel_user import panel_user_core
from app.helpers.error_helper import Error
from app.helpers.hash_helper import hash_helper
from app.models.panel_user import PanelUserLoginHistory, PanelUser
from app.schemas.admin.auth import ChangePasswordIn, AdminLoginIn, AdminLoginOut
from app.views.admin.deps import get_current_panel_user
from app.views.deps import get_db

router = APIRouter()


@router.post("/login", response_model=AdminLoginOut, summary="Giriş Yap")
def login(
    data: AdminLoginIn,
    db: Session = Depends(get_db),
):
    panel_user = panel_user_core.get_panel_user_by_email(db=db, email=data.email)
    if not panel_user:
        raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail=Error.invalid_login)

    if not hash_helper.verify(panel_user.password_hash, data.password):
        raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail=Error.invalid_login)


    login_result = auth_core.panel_user_login(panel_user=panel_user)

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    panel_user.login_histories.append(
        PanelUserLoginHistory(
            ip_address=ip_address,
            user_agent=user_agent,
        )
    )
    db.commit()
    return login_result


@router.put("/change-password", summary="Panel kullanıcısı şifre değiştirme")
def change_password(
    data: ChangePasswordIn, db: Session = Depends(get_db), current_user: PanelUser = Depends(get_current_panel_user)
):
    # Mevcut şifre doğrulaması
    if not hash_helper.verify(current_user.password_hash, data.current_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_current_password)

    # Yeni şifre eskiyle aynı mı?
    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Error.new_password_same_as_old,
        )

    # Yeni şifreyi hashleyip DB’ye kaydet
    current_user.password_hash = hash_helper.get_password_hash(data.new_password)
    db.commit()

    return {"message": "Şifre başarıyla güncellendi."}

