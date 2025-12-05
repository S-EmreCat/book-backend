from datetime import date

from app.enums import Status, StatusInput
from app.schemas.base import BaseSchema


class UserListOut(BaseSchema):
    id: int
    full_name: str
    email: str
    phone_number: str
    status: Status


class UserDetailOut(BaseSchema):
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


class UserStatusUpdateIn(BaseSchema):
    status: StatusInput
