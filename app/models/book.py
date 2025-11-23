from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.enums import Status
from app.models.base import Base


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

    Favorites = relationship("Favorite", back_populates="book", lazy="selectin")


# TODO: table: book_comment, book_rating, book_tag eklenebilir
# TODO: daha fazla field eklenebilir mi?
# TODO: panel_user_id eklenebilir; hangi admin tarafından oluşturulduğu bilgisi için
