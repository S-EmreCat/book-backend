from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.core.comment import comment_core
from app.enums import Status
from app.models.user import User
from app.schemas.pagination import CustomPage
from app.schemas.panel.book import BookDetailOut, BookListOut
from app.schemas.panel.comment import CommentIn, CommentOut
from app.views.deps import get_db
from app.views.panel.deps import get_current_panel_user

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


@router.post("/{book_id}/comment", response_model=CommentOut, summary="Kitaba yorum + rating ekle")
def create_comment(
    book_id: int,
    data: CommentIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_panel_user),
):
    return comment_core.create_comment(db=db, book_id=book_id, user=user, data=data)
