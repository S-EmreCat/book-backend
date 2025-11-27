from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base


class Favorite(Base):
    __tablename__ = "favorite"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "book_id", name="uq_favorite_user_book"),)

    user = relationship("User", foreign_keys=[user_id])
    book = relationship("Book", foreign_keys=[book_id])
