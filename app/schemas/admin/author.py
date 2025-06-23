from datetime import datetime
from typing import Optional

from app.enums import Status
from app.schemas.base import BaseSchema


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
