from datetime import datetime
from typing import Optional

from app.enums import Status
from app.schemas.base import BaseSchema


class BookIn(BaseSchema):
    title: str
    isbn: str
    author_id: int
    category_id: int
    published_year: Optional[int]
    page_count: Optional[int]
    barcode: int
    description: Optional[str]
    status: Optional[Status]


class BookOut(BaseSchema):
    id: int
    date_created: datetime
    date_modified: datetime
    title: str
    isbn: Optional[str]
    author_id: int
    category_id: int
    published_year: Optional[int]
    page_count: Optional[int]
    barcode: int
    description: Optional[str]
    status: Status


class BookListOut(BaseSchema):
    id: int
    title: str
    isbn: Optional[str]
    author_id: int
    category_id: int
    status: Status
