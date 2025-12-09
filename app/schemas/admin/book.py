from datetime import datetime
from typing import Optional

from pydantic import Field, field_validator

from app.enums import Status
from app.schemas.base import BaseSchema


class AuthorOut(BaseSchema):
    id: int
    name: str


class CategoryOut(BaseSchema):
    id: int
    name: str


class PublisherOut(BaseSchema):
    id: int
    name: str


class BookIn(BaseSchema):
    title: str = Field(min_length=2)
    isbn: str
    author_id: int
    category_id: int
    publisher_id: int
    published_year: Optional[int]
    page_count: Optional[int] = Field(default=None, ge=1)
    barcode: int = Field(ge=2)
    description: Optional[str]
    status: Optional[Status] = Status.passive

    @field_validator("published_year")
    @classmethod
    def validate_published_year(cls, year):
        if year is not None and year > datetime.now().year:
            raise ValueError("Yayın yılı gelecekte olamaz.")
        return year


class BookBase(BaseSchema):
    id: int
    title: str
    isbn: Optional[str]
    author: AuthorOut
    category: CategoryOut
    publisher: PublisherOut
    status: Status
    favorite_count: int


class BookOut(BookBase):
    date_created: datetime
    date_modified: datetime
    published_year: Optional[int]
    page_count: Optional[int]
    barcode: int
    description: Optional[str]


class BookListOut(BookBase):
    ...
