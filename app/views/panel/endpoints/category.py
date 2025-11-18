from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.category import category_core
from app.models import PanelUser
from app.schemas.panel.category import PanelCategoryOut
from app.views.admin.deps import get_current_panel_user
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=list[PanelCategoryOut], summary="Aktif Kategorileri Listele")
def get_categories(
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return category_core.get_all_active_categories(db=db)


@router.get("/{category_id}", response_model=PanelCategoryOut, summary="Kategori Detayı")
def get_category_detail(category_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_panel_user)):
    return category_core.get_category_by_id(db, category_id, only_active=True)
