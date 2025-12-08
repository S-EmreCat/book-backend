from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.core.author import author_core
from app.core.category import category_core
from app.enums import Status
from app.helpers.error_helper import Error
from app.models import Author, Book, Category, Favorite
from app.schemas.admin.book import BookIn


class BookCore:
    def __init__(self):
        pass

    def get_book_by_id(self, db: Session, book_id: int, only_active=True, with_entities=False):
        filter_array = [Book.id == book_id, Book.status != Status.deleted]
        if only_active:
            filter_array.append(Book.status == Status.active)

        query = db.query(Book).filter(*filter_array)

        if with_entities:
            query = (
                query.join(Author, Author.id == Book.author_id)
                .join(Category, Category.id == Book.category_id)
                .outerjoin(Favorite, Favorite.book_id == Book.id)
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
                    func.count(Favorite.id).label("favorite_count"),
                )
            )

        book = query.first()

        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error.book_not_found)
        return book

    def get_all_books(self, db: Session, search=None, status=None, with_entities=False, author_id=None):
        query = db.query(Book)
        filter_array = [Book.status != Status.deleted]

        if author_id is not None:
            filter_array.append(Book.author_id == author_id)

        if status is not None:
            filter_array.append(Book.status == status)

        if search:
            search = f"%{search}%"
            filter_array.append(
                or_(
                    Book.title.ilike(search),
                    Book.isbn.ilike(search),
                    Book.barcode.ilike(search),
                )
            )

        if with_entities:
            query = (
                query.join(Author, Author.id == Book.author_id)
                .join(Category, Category.id == Book.category_id)
                .outerjoin(Favorite, Favorite.book_id == Book.id)
                .with_entities(
                    Book.id.label("id"),
                    Book.date_created.label("date_created"),
                    Book.title.label("title"),
                    Author.name.label("author_name"),
                    Category.name.label("category_name"),
                    Book.published_year.label("published_year"),
                    func.count(Favorite.id).label("favorite_count"),
                )
                .group_by(Book.id)
            )

        return paginate(query.filter(*filter_array))

    def create_book(self, db: Session, data: BookIn):
        if data.isbn:
            exists = db.query(Book).filter(Book.isbn == data.isbn, Book.status != Status.deleted).first()
            if exists:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=Error.book_isbn_exists)

        author = author_core.get_author_by_id(db=db, author_id=data.author_id)
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
        return book

    def delete_book(self, db: Session, book_id: int):
        book = self.get_book_by_id(db=db, book_id=book_id, only_active=False)
        book.status = Status.deleted
        db.commit()
        return {"message": "Book deleted successfully."}


book_core = BookCore()
