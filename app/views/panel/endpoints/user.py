from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.user import user_core
from app.models.user import User
from app.schemas.panel.user import UserDetailOut, UserMeUpdateIn
from app.views.deps import get_db
from app.views.panel.deps import get_current_panel_user

router = APIRouter()


@router.get("/me", response_model=UserDetailOut, summary="Profilimi Görüntüle")
def get_me(
    panel_user: User = Depends(get_current_panel_user),
):
    return panel_user


@router.put("/me", response_model=UserMeUpdateIn, summary="Profilimi Güncelle")
def update_me(
    data: UserMeUpdateIn,
    db: Session = Depends(get_db),
    panel_user: User = Depends(get_current_panel_user),
):
    return user_core.update_me(db=db, user=panel_user, data=data)
