from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.author import author_core
from app.core.category import category_core
from app.enums import Status
from app.helpers.error_helper import Error
from app.models import Book
from app.models.author import Author
from app.models.category import Category
from app.schemas.admin.book import BookIn


class BookCore:
    def __init__(self):
        pass

    def get_book_by_id(self, db: Session, book_id: int, only_active=True):
        filter_array = [Book.id == book_id, Book.status != Status.deleted]
        if only_active:
            filter_array.append(Book.status == Status.active)
        book = db.query(Book).filter(*filter_array).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.record_not_found)
        return book

    def get_all_books(self, db: Session, search=None, status=None, with_entities=False):
        query = db.query(Book)

        if status is not None:
            query = query.filter(Book.status == status)
        else:
            query = query.filter(Book.status != Status.deleted)

        if search:
            search = f"%{search}%"
            query = query.filter(
                or_(
                    Book.title.ilike(search),
                    Book.isbn.ilike(search),
                    Book.barcode.ilike(search),
                )
            )

        if with_entities:
            favorite_count = Book.favorite_count.label("favorite_count")
            query = (
                query.with_entities(
                    Book.id.label("id"),
                    Book.date_created.label("date_created"),
                    Book.title.label("title"),
                    Author.name.label("author_name"),
                    Category.name.label("category_name"),
                    Book.published_year.label("published_year"),
                    favorite_count,
                )
                .join(Author, Author.id == Book.author_id)
                .join(Category, Category.id == Book.category_id)
            )
        return paginate(query)

    def get_active_book_detail(self, db: Session, book_id: int):
        """
        GET /panel/book/{book_id}
        Sadece aktif kitap + detay alanları + favorite count
        """
        favorite_count = Book.favorite_count.label("favorite_count")
        query = (
            db.query(Book)
            .join(Author, Author.id == Book.author_id)
            .join(Category, Category.id == Book.category_id)
            .filter(
                Book.id == book_id,
                Book.status == Status.active,
            )
            .with_entities(
                Book.id.label("id"),
                Book.date_created.label("date_created"),
                Book.title.label("title"),
                Author.name.label("author_name"),
                Category.name.label("category_name"),
                Book.published_year.label("published_year"),
                Book.page_count.label("page_count"),
                Book.isbn.label("isbn"),
                Book.barcode.label("barcode"),
                Book.description.label("description"),
                favorite_count,
            )
        )

        row = query.first()
        if not row:
            # kitap yoksa veya active değilse
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Error.record_not_found,
            )

        return row

    def create_book(self, db: Session, data: BookIn):
        # ISBN uniqueness check (excluding deleted - check active or passive)
        if data.isbn:
            exists = db.query(Book).filter(Book.isbn == data.isbn, Book.status != Status.deleted).first()
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=Error.book_isbn_exists,
                )

        # author_id controll
        author = author_core.get_author_by_id(db=db, author_id=data.author_id)
        # category_id controll
        category = category_core.get_category_by_id(db=db, category_id=data.category_id)

        book = Book(
            title=data.title,
            isbn=data.isbn,
            author_id=author.id,
            category_id=category.id,
            published_year=data.published_year,
            page_count=data.page_count,
            barcode=data.barcode,
            description=data.description,
            status=data.status,
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
