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


class BookIn(BaseSchema):
    title: str = Field(min_length=2)
    isbn: str
    author_id: int
    category_id: int
    published_year: Optional[int]
    page_count: Optional[int]
    barcode: int
    description: Optional[str]
    status: Optional[Status]

    @field_validator("published_year")
    @classmethod
    def validate_published_year(cls, year):
        if year is not None and year > datetime.now().year:
            raise ValueError("Yayın yılı gelecekte olamaz.")
        return year

    @field_validator("page_count")
    @classmethod
    def validate_page_count(cls, page_count):
        if page_count is not None and page_count <= 0:
            raise ValueError("Sayfa sayısı 0'dan büyük olmalıdır.")
        return page_count

    @field_validator("barcode")
    @classmethod
    def validate_barcode(cls, barcode):
        if barcode <= 0:
            raise ValueError("Barkod pozitif olmalıdır.")
        return barcode


class BookOut(BaseSchema):
    id: int
    date_created: datetime
    date_modified: datetime
    title: str
    isbn: Optional[str]
    author: AuthorOut
    category: CategoryOut
    published_year: Optional[int]
    page_count: Optional[int]
    barcode: int
    description: Optional[str]
    status: Status


class BookListOut(BaseSchema):
    id: int
    title: str
    isbn: Optional[str]
    author: AuthorOut
    category: CategoryOut
    status: Status
