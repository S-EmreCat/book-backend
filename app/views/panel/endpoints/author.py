from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.author import author_core
from app.models.panel_user import PanelUser
from app.schemas.panel.author import PanelAuthorDetailOut, PanelAuthorListOut
from app.views.admin.deps import get_current_panel_user
from app.views.deps import get_db

router = APIRouter()


@router.get(
    "",
    response_model=list[PanelAuthorListOut],
    summary="Aktif Yazarları Listele",
)
def get_authors(
    db: Session = Depends(get_db),
    current_user: PanelUser = Depends(get_current_panel_user),
):
    return author_core.get_active_authors(db=db)


@router.get("/{author_id}", response_model=PanelAuthorDetailOut, summary="Aktif Yazar Detayı")
def get_author_detail(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: PanelUser = Depends(get_current_panel_user),
):
    return author_core.get_author_by_id(db=db, author_id=author_id, only_active=True)
