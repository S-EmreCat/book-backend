from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import auth_core
from app.core.user import user_core
from app.models.user import User
from app.schemas.panel.auth import PanelLoginIn, PanelLoginOut, RegisterIn
from app.schemas.panel.user import UserDetailOut, UserMeUpdateIn
from app.views.deps import get_db
from app.views.panel.deps import get_current_panel_user

router = APIRouter()


@router.post("/register", summary="Kullanıcı kayıt")
def register(
    data: RegisterIn,
    db: Session = Depends(get_db),
):
    user_core.create_user(db=db, data=data)
    return {"message": "Kayıt başarıyla oluşturuldu."}


@router.post("/login", response_model=PanelLoginOut, summary="Kullanıcı girişi")
def login(
    data: PanelLoginIn,
    db: Session = Depends(get_db),
):
    user = user_core.authenticate_user(db=db, email=data.email, password=data.password)
    return auth_core.user_login(user=user)


@router.get("/me", response_model=UserDetailOut, summary="Profilimi Görüntüle")
def get_me(
    panel_user: User = Depends(get_current_panel_user),
):
    return user_core.get_me(panel_user)


@router.put("/me", response_model=UserMeUpdateIn, summary="Profilimi Güncelle")
def update_me(
    data: UserMeUpdateIn,
    db: Session = Depends(get_db),
    panel_user: User = Depends(get_current_panel_user),
):
    return user_core.update_me(db=db, user=panel_user, data=data)
