from datetime import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class AuthorOut(BaseSchema):
    id: int
    name: str


class CategoryOut(BaseSchema):
    id: int
    name: str


class PanelBookListOut(BaseSchema):
    id: int
    date_created: datetime
    title: str
    author_name: str | None = None
    category_name: str | None = None
    published_year: Optional[int]


class PanelBookOut(BaseSchema):
    id: int
    date_created: datetime
    title: str
    author_name: str | None = None
    category_name: str | None = None
    published_year: Optional[int]
    page_count: Optional[int]
    isbn: str
    barcode: int
    description: Optional[str]
