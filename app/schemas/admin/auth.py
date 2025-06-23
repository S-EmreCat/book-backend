from datetime import datetime
from typing import Optional

from pydantic import Field

from app.enums import Status
from app.schemas.base import BaseSchema


class LoginIn(BaseSchema):
    email: str = Field(example="sample@sample.com")
    password: str = Field(example="Admin1234")


class LoginOut(BaseSchema):
    access_token: str


class AuthorIn(BaseSchema):
    name: str
    description: Optional[str]
    image_url: Optional[str]
    status: Optional[Status]


class AuthorOut(BaseSchema):
    id: int
    date_created: datetime
    date_modified: datetime
    name: str
    description: Optional[str]
    image_url: Optional[str]
    status: Status
