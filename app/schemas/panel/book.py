from datetime import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class BookBase(BaseSchema):
    id: int
    date_created: datetime
    title: str
    author_name: str
    category_name: str
    publisher_name: str
    published_year: Optional[int]
    favorite_count: int


class BookDetailOut(BookBase):
    page_count: Optional[int]
    isbn: Optional[str]
    barcode: int
    description: Optional[str]


class BookListOut(BookBase):
    ...
