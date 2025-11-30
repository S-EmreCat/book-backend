from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.author import author_core
from app.core.book import book_core
from app.enums import Status
from app.models.user import User
from app.schemas.pagination import CustomPage
from app.schemas.panel.author import PanelAuthorDetailOut, PanelAuthorListOut
from app.schemas.panel.book import BookListOut
from app.views.deps import get_db
from app.views.panel.deps import get_current_panel_user

router = APIRouter()


@router.get(
    "",
    response_model=CustomPage[PanelAuthorListOut],
    summary="Aktif Yazarları Listele",
)
def get_authors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_panel_user),
):
    return author_core.get_all_authors(db=db, status=Status.active)


@router.get("/{author_id}", response_model=PanelAuthorDetailOut, summary="Aktif Yazar Detayı")
def get_author_detail(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_panel_user),
):
    return author_core.get_author_by_id(db=db, author_id=author_id, only_active=True)


@router.get(
    "/{author_id}/books",
    response_model=CustomPage[BookListOut],
    summary="Yazarın kitaplarını listele",
)
def get_author_books(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_panel_user),
):
    author_core.get_author_by_id(db=db, author_id=author_id, only_active=True)

    return book_core.get_all_books(db=db, with_entities=True, author_id=author_id, status=Status.active)
