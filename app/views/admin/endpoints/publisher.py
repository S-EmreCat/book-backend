from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.publisher import publisher_core
from app.schemas import MessageOut
from app.schemas.admin.publisher import PublisherIn, PublisherOut
from app.schemas.pagination import CustomPage
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=CustomPage[PublisherOut], summary="Tüm Yayınevlerini Listele")
def get_all_publishers(
    db: Session = Depends(get_db),
):
    return publisher_core.get_all_publishers(db=db, only_active=False)


@router.get("/{publisher_id}", response_model=PublisherOut, summary="Yayınevi Detayı")
def get_publisher_detail(
    publisher_id: int,
    db: Session = Depends(get_db),
):
    return publisher_core.get_publisher_by_id(db=db, publisher_id=publisher_id, only_active=False)


@router.post("", response_model=PublisherOut, summary="Yayınevi Ekle")
def create_publisher(
    data: PublisherIn,
    db: Session = Depends(get_db),
):
    return publisher_core.create_publisher(db=db, data=data)


@router.put("/{publisher_id}", response_model=PublisherOut, summary="Yayınevi Güncelle")
def update_publisher(
    publisher_id: int,
    data: PublisherIn,
    db: Session = Depends(get_db),
):
    return publisher_core.update_publisher(db=db, publisher_id=publisher_id, data=data)


@router.delete("/{publisher_id}", response_model=MessageOut, summary="Yayınevi Sil")
def delete_publisher(
    publisher_id: int,
    db: Session = Depends(get_db),
):
    return publisher_core.delete_publisher(db=db, publisher_id=publisher_id)
