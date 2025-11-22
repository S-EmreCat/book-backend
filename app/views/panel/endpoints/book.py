from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.schemas.panel.book import BookDetailOut, BookListOut
from app.views.deps import get_db
from app.views.panel.deps import get_current_panel_user

router = APIRouter()


@router.get(
    "",
    response_model=list[BookListOut],
    summary="Aktif kitapları listele",
)
def get_all_active_books(
    db: Session = Depends(get_db),
    panel_user=Depends(get_current_panel_user),
):
    return book_core.get_all_books(db=db, query=True)


@router.get(
    "/{book_id}",
    response_model=BookDetailOut,
    summary="Aktif kitap detayını göster",
)
def get_active_book_detail(
    book_id: int,
    db: Session = Depends(get_db),
    panel_user=Depends(get_current_panel_user),
):
    return book_core.get_active_book_detail(db=db, book_id=book_id)
