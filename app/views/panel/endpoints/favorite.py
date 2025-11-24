from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.core.favorite import favorite_core
from app.models import User
from app.schemas import MessageOut
from app.schemas.pagination import CustomPage
from app.schemas.panel.book import BookListOut
from app.views.deps import get_db
from app.views.panel.deps import get_current_panel_user

router = APIRouter()


@router.get("/", response_model=CustomPage[BookListOut], summary="Favori Kitaplarını Listele")
def get_favorite_books(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_panel_user),
):
    query = favorite_core.get_user_favorite_books_query(db=db, user=user)
    return paginate(query)


@router.post("/{book_id}", response_model=MessageOut, summary="Favorilere Kitap Ekle")
def add_favorite_book(
    book_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_panel_user),
):
    favorite_core.add_favorite(db=db, user=user, book_id=book_id)
    return MessageOut(message="Favorilere kitap ekle")


@router.delete("/{book_id}", response_model=MessageOut, summary="Favori Kitaplarından Çıkar")
def remove_favorite_book(
    book_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_panel_user),
):
    favorite_core.remove_favorite(db=db, user=user, book_id=book_id)
    return MessageOut(message="Favorilerden kitap çıkarıldı")
