from datetime import date

from app.enums import Status
from app.schemas.base import BaseSchema


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


class UserMeUpdateIn(BaseSchema):
    first_name: str
    last_name: str
    birth_date: date
