from datetime import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class FavoriteOut(BaseSchema):
    id: int
    date_created: datetime
    book_id: int
    title: str
    author_name: str
    category_name: str
    published_year: Optional[int]
