from sqlalchemy import Column, Enum, String

from app.enums import Status
from app.models.base import Base


class Category(Base):
    __tablename__ = "category"

    name = Column(String(50), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.active)


# TODO: sub_category olmalı mı?
