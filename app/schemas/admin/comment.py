from datetime import datetime

from pydantic import Field

from app.enums import CommentRejectionReason, CommentStatus, CommentStatusInput
from app.schemas.base import BaseSchema


class CommentListOut(BaseSchema):
    id: int
    date_created: datetime
    book_id: int
    user_id: int
    user_name: str
    rating: int
    status: CommentStatus


class CommentOut(BaseSchema):
    id: int
    date_created: datetime
    book_id: int
    user_id: int
    user_name: str
    rating: int
    comment: str
    is_visible: bool
    status: CommentStatus
    rejection_reason: str | None
    submitted_by_id: int | None


class CommentStatusIn(BaseSchema):
    status: CommentStatusInput = Field(example=CommentStatusInput.approved)
    reason_enum: CommentRejectionReason | None = Field(default=None, example=CommentRejectionReason.spam)
    reason_text: str | None = Field(default=None, example="Reklam / alakasız içerik.")
