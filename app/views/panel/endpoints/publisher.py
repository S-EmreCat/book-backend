from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.publisher import publisher_core
from app.models import User
from app.schemas.pagination import CustomPage
from app.schemas.panel.publisher import PanelPublisherOut
from app.views.deps import get_db
from app.views.panel.deps import get_current_panel_user

router = APIRouter()


@router.get("", response_model=CustomPage[PanelPublisherOut], summary="Aktif Yayın Evlerini Listele")
def get_publishers(
    db: Session = Depends(get_db),
    panel_user: User = Depends(get_current_panel_user),
):
    return publisher_core.get_all_publishers(db=db)


@router.get("/{publisher_id}", response_model=PanelPublisherOut, summary="Yayın Evi Detayı")
def get_publisher_detail(
    publisher_id: int,
    db: Session = Depends(get_db),
    panel_user=Depends(get_current_panel_user),
):
    return publisher_core.get_publisher_by_id(db, publisher_id)
