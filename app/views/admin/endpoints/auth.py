from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import auth_core
from app.core.panel_user import panel_user_core
from app.helpers.error_helper import Error
from app.helpers.hash_helper import hash_helper
from app.models import PanelUser
from app.schemas import MessageOut
from app.schemas.admin.auth import AuthorIn, AuthorOut, LoginIn, LoginOut
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


@router.get("", response_model=list[AuthorOut], summary="Tüm Yazarları Listele")
def get_all_authors(
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return auth_core.get_all_authors(db=db)


@router.get("/{author_id}", response_model=AuthorOut, summary="Yazar Detayı")
def get_author_detail(
    author_id: int,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return auth_core.get_author_by_id(db=db, author_id=author_id, only_active=False)


@router.post("", response_model=AuthorOut, summary="Yeni Yazar Ekle")
def create_author(
    data: AuthorIn,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return auth_core.create_author(db=db, data=data)


@router.put("/{author_id}", response_model=AuthorOut, summary="Yazar Güncelle")
def update_author(
    author_id: int,
    data: AuthorIn,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return auth_core.update_author(db=db, author_id=author_id, data=data)


@router.delete("/{author_id}", response_model=MessageOut, summary="Yazar Sil")
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return auth_core.delete_author(db=db, author_id=author_id)
