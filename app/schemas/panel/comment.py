from datetime import datetime

from pydantic import Field

from app.enums import CommentStatus
from app.schemas.base import BaseSchema


class CommentIn(BaseSchema):
    rating: int = Field(ge=1, le=5, example=5)
    comment: str = Field(min_length=1, max_length=2000, example="Çok beğendim.")
    is_visible: bool = Field(example=True)


class CommentOut(BaseSchema):
    id: int
    date_created: datetime
    book_id: int
    rating: int | None
    comment: str | None
    is_visible: bool
    status: CommentStatus
    rejection_reason: str | None


class CommentListOut(CommentOut):
    ...
