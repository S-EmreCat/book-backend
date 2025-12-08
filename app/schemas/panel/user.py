from datetime import date

from app.enums import Status
from app.schemas.base import BaseSchema


class UserBase(BaseSchema):
    first_name: str
    last_name: str
    birth_date: date


class UserDetailOut(UserBase):
    id: int
    full_name: str
    email: str
    phone_number: str
    email_verification: bool
    phone_verification: bool
    status: Status


class UserMeUpdateIn(UserBase):
    ...
