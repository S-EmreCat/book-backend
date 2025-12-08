from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.category import category_core
from app.schemas.pagination import CustomPage
from app.schemas.panel.category import PanelCategoryOut
from app.views.deps import get_db

router = APIRouter()


@router.get(
    "",
    response_model=CustomPage[PanelCategoryOut],
    summary="Tüm Kategorileri Listele",
)
def get_categories(
    db: Session = Depends(get_db),
):
    return category_core.get_all_categories(db=db)


@router.get("/{category_id}", response_model=PanelCategoryOut, summary="Kategori Detayı")
def get_category_detail(
    category_id: int,
    db: Session = Depends(get_db),
):
    return category_core.get_category_by_id(db=db, category_id=category_id)
