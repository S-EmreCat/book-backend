import traceback

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import auth_core
from app.core.panel_user import panel_user_core
from app.helpers.error_helper import Error
from app.helpers.hash_helper import hash_helper
from app.models.panel_user import PanelUser
from app.schemas.admin.auth import ChangePasswordIn, LoginIn, LoginOut
from app.views.admin.deps import get_current_panel_user
from app.views.deps import get_db

router = APIRouter()


@router.post("/login", response_model=LoginOut, summary="Giriş Yap")
def login(
    data: LoginIn,
    db: Session = Depends(get_db),
):
    panel_user = panel_user_core.get_panel_user_by_email(db=db, email=data.email)
    if not panel_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_login)

    if not hash_helper.verify(panel_user.password_hash, data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_login)

    return auth_core.panel_user_login(panel_user=panel_user)


@router.put("/change-password", summary="Panel kullanıcısı şifre değiştirme")
def change_password(
    data: ChangePasswordIn, db: Session = Depends(get_db), current_user: PanelUser = Depends(get_current_panel_user)
):
    try:
        # current_user kontrolü
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=Error.invalid_login)

        # Mevcut şifre doğrulaması
        if not hash_helper.verify(current_user.password_hash, data.current_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_current_password)

        # Yeni şifre eskiyle aynı mı kontrol
        if hash_helper.verify(current_user.password_hash, data.new_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.new_password_same_as_old)

        # Yeni şifreyi hashleyip DB’ye kaydet
        current_user.password_hash = hash_helper.get_password_hash(data.new_password)
        db.commit()
        db.refresh(current_user)

        return {"message": "Şifre başarıyla güncellendi."}

    except HTTPException:
        raise  # Zaten uygun hata kodları fırlatıldı
    except Exception:
        # Hata loglama
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
