from datetime import datetime
from typing import Optional

from app.enums import Status
from app.schemas.base import BaseSchema


class PublisherIn(BaseSchema):
    name: str
    status: Optional[Status] = Status.passive


class PublisherOut(BaseSchema):
    id: int
    date_created: datetime
    date_modified: datetime
    name: str
    status: Status
