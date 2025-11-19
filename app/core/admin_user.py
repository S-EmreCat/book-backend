from typing import Optional

from sqlalchemy.orm import Session

from app.enums import Status
from app.models import AdminUser


class AdminUserCore:
    def __init__(self):
        pass

    def get_admin_user_by_email(self, db: Session, email: str) -> Optional[AdminUser]:
        return db.query(AdminUser).filter(AdminUser.email == email, AdminUser.status == Status.active).first()


admin_user_core = AdminUserCore()
