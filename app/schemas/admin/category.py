from datetime import datetime
from typing import Optional

from app.enums import Status
from app.schemas.base import BaseSchema


class CategoryIn(BaseSchema):
    name: str
    status: Optional[Status]


class CategoryOut(BaseSchema):
    id: int
    date_created: datetime
    date_modified: datetime
    name: str
    status: Status
