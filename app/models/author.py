from sqlalchemy import Column, Enum, String, Text

from app.enums import Status
from app.models.base import Base


class Author(Base):
    __tablename__ = "author"

    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(200), nullable=True)
    status = Column(Enum(Status), nullable=False, default=Status.passive)
