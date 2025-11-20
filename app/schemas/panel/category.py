from app.schemas.base import BaseSchema


class PanelCategoryOut(BaseSchema):
    id: int
    name: str
