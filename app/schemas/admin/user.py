from datetime import date

from app.enums import Status
from app.schemas.base import BaseSchema


class AdminUserListOut(BaseSchema):
    id: int
    full_name: str
    email: str
    phone_number: str


class AdminUserDetailOut(BaseSchema):
    id: int
    first_name: str
    last_name: str
    full_name: str
    email: str
    phone_number: str
    birth_date: date
    email_verification: bool
    phone_verification: bool
    status: Status


class AdminUserStatusUpdateIn(BaseSchema):
    status: Status
