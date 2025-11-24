from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.favorite import favorite_core
from app.models import User
from app.schemas import MessageOut
from app.schemas.pagination import CustomPage
from app.schemas.panel.favorite import FavoriteOut
from app.views.deps import get_db
from app.views.panel.deps import get_current_panel_user

router = APIRouter()


@router.get("/", response_model=CustomPage[FavoriteOut], summary="Favori Kitaplarını Listele")
def get_favorite_books(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_panel_user),
):
    return favorite_core.get_user_favorite_books(db=db, user=user)


@router.post("/{book_id}", response_model=FavoriteOut, summary="Favorilere Kitap Ekle")
def add_favorite_book(
    book_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_panel_user),
):
    return favorite_core.add_favorite(db=db, user=user, book_id=book_id)


@router.delete("/{book_id}", response_model=MessageOut, summary="Favori Kitaplarından Çıkar")
def remove_favorite_book(
    book_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_panel_user),
):
    return favorite_core.remove_favorite(db=db, user=user, book_id=book_id)
