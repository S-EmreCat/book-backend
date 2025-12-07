from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.publisher import publisher_core
from app.models import AdminUser
from app.schemas import MessageOut
from app.schemas.admin.publisher import PublisherIn, PublisherOut
from app.schemas.pagination import CustomPage
from app.views.admin.deps import get_current_admin_user
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=CustomPage[PublisherOut], summary="Tüm Yayın Evlerini Listele")
def get_all_publishers(
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return publisher_core.get_all_publishers(db=db, only_active=False)


@router.get("/{publisher_id}", response_model=PublisherOut, summary="Yayın Evi Detayı")
def get_publisher_detail(
    publisher_id: int,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return publisher_core.get_publisher_by_id(db=db, publisher_id=publisher_id, only_active=False)


@router.post("", response_model=PublisherOut, summary="Yayın Evi Ekle")
def create_publisher(
    data: PublisherIn,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return publisher_core.create_publisher(db=db, data=data)


@router.put("/{publisher_id}", response_model=PublisherOut, summary="Yayın Evi Güncelle")
def update_publisher(
    publisher_id: int,
    data: PublisherIn,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return publisher_core.update_publisher(db=db, publisher_id=publisher_id, data=data)


@router.delete("/{publisher_id}", response_model=MessageOut, summary="Yayın Evi Sil")
def delete_publisher(
    publisher_id: int,
    db: Session = Depends(get_db),
    panel_user: AdminUser = Depends(get_current_admin_user),
):
    return publisher_core.delete_publisher(db=db, publisher_id=publisher_id)
