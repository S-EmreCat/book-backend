from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import relationship

from app.enums import Status
from app.models.base import Base


class Publisher(Base):
    __tablename__ = "publisher"

    name = Column(String(256), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.active)

    books = relationship("Book", back_populates="publisher")
