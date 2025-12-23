from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.enums import CommentStatus
from app.models.base import Base


class BookComment(Base):
    __tablename__ = "book_comment"

    status = Column(Enum(CommentStatus), nullable=False, default=CommentStatus.pending)
    comment = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    is_visible = Column(Boolean, nullable=False, default=True)
    rejection_reason = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    submitted_by_id = Column(Integer, ForeignKey("admin_user.id"), nullable=True)

    book = relationship("Book", back_populates="comments", foreign_keys=[book_id])
    admin_user = relationship("AdminUser", back_populates="comments", foreign_keys=[submitted_by_id])
    user = relationship("User", back_populates="comments", foreign_keys=[user_id])
