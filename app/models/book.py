from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.enums import Status
from app.models.base import Base
from app.models.favorite import Favorite


class Book(Base):
    __tablename__ = "book"

    title = Column(String(256), nullable=False)
    isbn = Column(String(20), nullable=True)  # Uluslararası standart kitap numarası
    author_id = Column(Integer, ForeignKey("author.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

    published_year = Column(Integer, nullable=True)
    page_count = Column(Integer, nullable=True)

    barcode = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(Status), nullable=False, default=Status.passive)

    category = relationship("Category", foreign_keys=[category_id])
    author = relationship("Author", uselist=False)

    favorites = relationship("Favorite", back_populates="book", lazy="selectin")

    @hybrid_property
    def favorite_count(self) -> int:
        return len(self.favorites or [])

    @favorite_count.expression
    def favorite_count(cls):
        # Query tarafında: SQL COUNT
        return select(func.count(Favorite.id)).where(Favorite.book_id == cls.id).correlate(cls).scalar_subquery()


# TODO: table: book_comment, book_rating, book_tag eklenebilir
# TODO: daha fazla field eklenebilir mi?
# TODO: panel_user_id eklenebilir; hangi admin tarafından oluşturulduğu bilgisi için
