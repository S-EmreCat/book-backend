from typing import Optional

from sqlalchemy.orm import Session

from app.enums import Status
from app.models import PanelUser


class PanelUserCore:
    def __init__(self):
        pass

    def get_panel_user_by_email(self, db: Session, email: str) -> Optional[PanelUser]:
        return db.query(PanelUser).filter(PanelUser.email == email, PanelUser.status == Status.active).first()


panel_user_core = PanelUserCore()
