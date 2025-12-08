from typing import Optional

from app.schemas.base import BaseSchema


class AuthorListOut(BaseSchema):
    id: int
    name: str
    image_url: Optional[str]


class AuthorDetailOut(BaseSchema):
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
