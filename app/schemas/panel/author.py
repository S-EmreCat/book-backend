from typing import Optional

from app.schemas.base import BaseSchema


class PanelAuthorListOut(BaseSchema):
    id: int
    name: str
    image_url: Optional[str]


class PanelAuthorDetailOut(BaseSchema):
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
