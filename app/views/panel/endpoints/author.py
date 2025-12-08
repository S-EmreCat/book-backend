from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.author import author_core
from app.core.book import book_core
from app.enums import Status
from app.schemas.pagination import CustomPage
from app.schemas.panel.author import AuthorDetailOut, AuthorListOut
from app.schemas.panel.book import BookListOut
from app.views.deps import get_db

router = APIRouter()


@router.get(
    "",
    response_model=CustomPage[AuthorListOut],
    summary="Tüm Yazarları Listele",
)
def get_authors(db: Session = Depends(get_db)):
    return author_core.get_all_authors(db=db)


@router.get("/{author_id}", response_model=AuthorDetailOut, summary="Yazar Detayı")
def get_author_detail(author_id: int, db: Session = Depends(get_db)):
    return author_core.get_author_by_id(db=db, author_id=author_id)


@router.get(
    "/{author_id}/books",
    response_model=CustomPage[BookListOut],
    summary="Yazarın kitaplarını listele",
)
def get_author_books(author_id: int, db: Session = Depends(get_db)):
    author_core.get_author_by_id(db=db, author_id=author_id)
    return book_core.get_all_books(db=db, with_entities=True, author_id=author_id, status=Status.active)
