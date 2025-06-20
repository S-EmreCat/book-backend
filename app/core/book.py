from fastapi import HTTPException, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, joinedload

from app.enums import Status
from app.helpers.error_helper import Error
from app.models import Book
from app.schemas.admin.book import BookIn


class BookCore:
    def __init__(self):
        pass

    def get_book_by_id(self, db: Session, book_id: int, only_active=True):
        filter_array = [Book.id == book_id, Book.status != Status.deleted]
        if only_active:
            filter_array.append(Book.status == Status.active)
        book = db.query(Book).filter(*filter_array).options(joinedload(Book.author), joinedload(Book.category)).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.record_not_found)
        return book

    def get_all_books(self, db: Session, search=None, status=None):
        filter_array = []
        if search:
            search = f"%{search}%"
            filter_array.append(
                or_(
                    Book.title.ilike(search),
                    Book.isbn.ilike(search),
                    Book.barcode.ilike(search),
                )
            )

        if status is not None:
            filter_array.append(and_(Book.status == status))
        else:
            filter_array.append(and_(Book.status != Status.deleted))

        return db.query(Book).filter(*filter_array).options(joinedload(Book.author), joinedload(Book.category)).all()

    def create_book(self, db: Session, data: BookIn):
        book = Book(
            title=data.title,
            isbn=data.isbn,
            author_id=data.author_id,
            category_id=data.category_id,
            published_year=data.published_year,
            page_count=data.page_count,
            barcode=data.barcode,
            description=data.description,
        )
        db.add(book)
        db.commit()
        return book

    def update_book(self, db: Session, book_id: int, data: BookIn):
        book = self.get_book_by_id(db=db, book_id=book_id, only_active=False)

        book.title = data.title
        book.isbn = data.isbn
        book.author_id = data.author_id
        book.category_id = data.category_id
        book.published_year = data.published_year
        book.page_count = data.page_count
        book.barcode = data.barcode
        book.description = data.description
        book.status = data.status

        db.commit()
        db.refresh(book)
        return book

    def delete_book(self, db: Session, book_id: int):
        book = self.get_book_by_id(db=db, book_id=book_id, only_active=False)
        book.status = Status.deleted
        db.commit()
        return {"message": "Book deleted successfully."}


book_core = BookCore()
