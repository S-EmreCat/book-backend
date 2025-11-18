from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.models import PanelUser
from app.schemas.panel.book import PanelBookListOut, PanelBookOut
from app.views.admin.deps import get_current_panel_user
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=list[PanelBookListOut], summary="Aktif Kitapları Listele")
def get_active_books(
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    books = book_core.gel_active_books(db=db)

    return [
        PanelBookListOut(
            id=book.id,
            date_created=book.date_created,
            title=book.title,
            author_name=book.author.name if book.author else None,
            category_name=book.category.name if book.category else None,
            published_year=book.published_year,
        )
        for book in books
    ]


@router.get("/{book_id}", response_model=PanelBookOut, summary="Aktif Kitap Detayı")
def get_active_book_detail(
    book_id: int,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    book = book_core.get_book_by_id(db=db, book_id=book_id, only_active=True)

    return PanelBookOut(
        id=book.id,
        date_created=book.date_created,
        title=book.title,
        author_name=book.author.name if book.author else None,
        category_name=book.category.name if book.category else None,
        published_year=book.published_year,
        page_count=book.page_count,
        isbn=book.isbn,
        barcode=book.barcode,
        description=book.description,
    )
