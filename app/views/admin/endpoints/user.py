from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.user import user_core
from app.enums import Status
from app.models import AdminUser
from app.schemas.admin.user import UserDetailOut, UserListOut, UserStatusUpdateIn
from app.schemas.pagination import CustomPage
from app.views.admin.deps import get_current_admin_user
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=CustomPage[UserListOut], summary="Tüm Kullanıcıları Listele")
def get_all_users(
    email: str | None = Query(default=None, description="Email ile filtrele", example="sample@sample.com"),
    phone_number: str | None = Query(default=None, description="Telefon ile filtrele", example="905321234567"),
    status: Status | None = Query(default=None, description="Status ile filtrele", example="active"),
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return user_core.get_user_list(db=db, email=email, phone_number=phone_number, status=status)


@router.get("/{user_id}", response_model=UserDetailOut, summary="Panel kullanıcı detayını getir")
def get_panel_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return user_core.get_user_by_id(db=db, user_id=user_id)


@router.put("/{user_id}", response_model=UserDetailOut, summary="Panel kullanıcının status alanını güncelle")
def update_panel_user_status(
    user_id: int,
    data: UserStatusUpdateIn,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return user_core.update_user(db=db, user_id=user_id, new_status=data.status)
