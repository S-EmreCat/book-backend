from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.user import user_core
from app.models import AdminUser
from app.schemas.admin.user import AdminUserListOut
from app.views.admin.deps import get_current_admin_user
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=list[AdminUserListOut], summary="Tüm Kullanıcıları Listele")
def get_all_users(
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return user_core.get_user_list(db=db)
