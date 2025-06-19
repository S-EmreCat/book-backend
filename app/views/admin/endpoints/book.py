from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.models import PanelUser
from app.schemas import MessageOut
from app.schemas.admin.book import BookIn, BookListOut, BookOut
from app.views.admin.deps import get_current_panel_user
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=list[BookListOut], summary="Tüm Kitapları Listele")
def get_all_books(
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return book_core.get_all_books(db=db)


@router.get("/{book_id}", response_model=BookListOut, summary="Kitap Detayı")
def get_book_detail(
    book_id: int,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return book_core.get_book_by_id(db=db, book_id=book_id, only_active=False)


@router.post("", response_model=BookOut, summary="Kitap Ekle")
def create_book(
    data: BookIn,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return book_core.create_book(db=db, data=data)


@router.put("/{book_id}", response_model=BookOut, summary="Kitap Güncelle")
def update_book(
    book_id: int,
    data: BookIn,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return book_core.update_book(db=db, book_id=book_id, data=data)


@router.delete("/{book_id}", response_model=MessageOut, summary="Kitap Sil")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return book_core.delete_book(db=db, book_id=book_id)
