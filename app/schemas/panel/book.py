from datetime import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class BookListOut(BaseSchema):
    id: int
    date_created: datetime
    title: str
    author_name: str
    category_name: str
    publisher_name: Optional[str]
    published_year: Optional[int]


class BookDetailOut(BaseSchema):
    id: int
    date_created: datetime
    title: str
    author_name: str
    category_name: str
    publisher_name: Optional[str]
    published_year: Optional[int]
    page_count: Optional[int]
    isbn: Optional[str]
    barcode: int
    description: Optional[str]
