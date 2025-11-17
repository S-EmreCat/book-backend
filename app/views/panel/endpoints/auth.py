from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import auth_core
from app.core.user import user_core
from app.schemas.panel.auth import PanelLoginIn, PanelLoginOut, RegisterIn
from app.views.deps import get_db

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
