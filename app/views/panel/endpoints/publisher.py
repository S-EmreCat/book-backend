from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.publisher import publisher_core
from app.schemas.pagination import CustomPage
from app.schemas.panel.publisher import PublisherOut
from app.views.deps import get_db

router = APIRouter()


@router.get("", response_model=CustomPage[PublisherOut], summary="Tüm Yayınevlerini Listele")
def get_publishers(
    db: Session = Depends(get_db),
):
    return publisher_core.get_all_publishers(db=db)


@router.get("/{publisher_id}", response_model=PublisherOut, summary="Yayınevi Detayı")
def get_publisher_detail(
    publisher_id: int,
    db: Session = Depends(get_db),
):
    return publisher_core.get_publisher_by_id(db, publisher_id)
