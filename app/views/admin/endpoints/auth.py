from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.admin_user import admin_user_core
from app.core.auth import auth_core
from app.helpers.error_helper import Error
from app.helpers.hash_helper import hash_helper
from app.models import AdminUser, AdminUserLoginHistory
from app.schemas.admin.auth import AdminLoginIn, AdminLoginOut, ChangePasswordIn
from app.views.admin.deps import get_current_admin_user
from app.views.deps import get_db

router = APIRouter()


@router.post("/login", response_model=AdminLoginOut, summary="Giriş Yap")
def login(
    data: AdminLoginIn,
    request: Request,
    db: Session = Depends(get_db),
):
    admin_user = admin_user_core.get_admin_user_by_email(db=db, email=data.email)
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_login)

    if not hash_helper.verify(admin_user.password_hash, data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=Error.invalid_login)

    login_result = auth_core.admin_user_login(admin_user=admin_user)

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    admin_user.login_histories.append(
        AdminUserLoginHistory(
            ip_address=ip_address,
            user_agent=user_agent,
        )
    )
    db.commit()
    return login_result


@router.put("/change-password", summary="Panel kullanıcısı şifre değiştirme")
def change_password(
    data: ChangePasswordIn,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_admin_user),
):
    if not hash_helper.verify(current_user.password_hash, data.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Error.invalid_current_password,
        )

    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Error.new_password_same_as_old,
        )

    current_user.password_hash = hash_helper.get_password_hash(data.new_password)
    db.commit()

    return {"message": "Şifre başarıyla güncellendi."}
