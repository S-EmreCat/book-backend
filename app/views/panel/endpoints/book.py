from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.enums import Status
from app.schemas.pagination import CustomPage
from app.schemas.panel.book import BookDetailOut, BookListOut
from app.views.deps import get_db

router = APIRouter()


@router.get(
    "",
    response_model=CustomPage[BookListOut],
    summary="Tüm Kitapları listele",
)
def get_all_active_books(db: Session = Depends(get_db)):
    return book_core.get_all_books(db=db, with_entities=True, status=Status.active)


@router.get(
    "/{book_id}",
    response_model=BookDetailOut,
    summary="Kitap Detayı",
)
def get_active_book_detail(book_id: int, db: Session = Depends(get_db)):
    return book_core.get_book_by_id(db=db, book_id=book_id, with_entities=True)
