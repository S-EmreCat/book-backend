from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.author import author_core
from app.models import AdminUser
from app.schemas import MessageOut
from app.schemas.admin.author import AuthorIn, AuthorOut
from app.views.admin.deps import get_current_admin_user
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=list[AuthorOut], summary="Tüm Yazarları Listele")
def get_all_authors(
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return author_core.get_all_authors(db=db)


@router.get("/{author_id}", response_model=AuthorOut, summary="Yazar Detayı")
def get_author_detail(
    author_id: int,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return author_core.get_author_by_id(db=db, author_id=author_id, only_active=False)


@router.post("", response_model=AuthorOut, summary="Yeni Yazar Ekle")
def create_author(
    data: AuthorIn,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return author_core.create_author(db=db, data=data)


@router.put("/{author_id}", response_model=AuthorOut, summary="Yazar Güncelle")
def update_author(
    author_id: int,
    data: AuthorIn,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return author_core.update_author(db=db, author_id=author_id, data=data)


@router.delete("/{author_id}", response_model=MessageOut, summary="Yazar Sil")
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return author_core.delete_author(db=db, author_id=author_id)
