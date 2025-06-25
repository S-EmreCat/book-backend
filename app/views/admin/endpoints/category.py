from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.category import category_core
from app.models import PanelUser
from app.schemas import MessageOut
from app.schemas.admin.category import CategoryIn, CategoryOut
from app.views.admin.deps import get_current_panel_user
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=list[CategoryOut], summary="Tüm Kategorileri Listele")
def get_all_categories(
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return category_core.get_all_categories(db=db)


@router.get("/{category_id}", response_model=CategoryOut, summary="Kategori Detayı")
def get_category_detail(
    category_id: int,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return category_core.get_category_by_id(db=db, category_id=category_id, only_active=False)


@router.post("", response_model=CategoryOut, summary="Kategori Ekle")
def create_category(
    data: CategoryIn,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return category_core.create_category(db=db, data=data)


@router.put("/{category_id}", response_model=CategoryOut, summary="Kategori Güncelle")
def update_category(
    category_id: int,
    data: CategoryIn,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return category_core.update_category(db=db, category_id=category_id, data=data)


@router.delete("/{category_id}", response_model=MessageOut, summary="Kategori Sil")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    panel_user: PanelUser = Depends(get_current_panel_user),
):
    return category_core.delete_category(db=db, category_id=category_id)
