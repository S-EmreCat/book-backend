from fastapi import HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.helpers.error_helper import Error
from app.models import Book, Favorite, User
from app.models.author import Author
from app.models.category import Category


class FavoriteCore:
    def __init__(self) -> None:
        pass

    def get_favorite(self, db: Session, user_id: int, book_id: int, raise_error: bool = True):
        query = (
            db.query(Favorite)
            .filter(
                Favorite.user_id == user_id,
                Favorite.book_id == book_id,
            )
            .first()
        )
        if not query and raise_error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Error.record_not_found,
            )
        return query

    def create_favorite(self, db: Session, user: User, book_id: int):
        # Kitap var mı ve aktif mi?
        book_core.get_book_by_id(db=db, book_id=book_id, only_active=True)

        # Favori mi?
        exists = self.get_favorite(db=db, user_id=user.id, book_id=book_id, raise_error=False)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Error.favorite_already_exists,
            )
        favorite = Favorite(user_id=user.id, book_id=book_id)
        db.add(favorite)
        db.commit()

        return (
            db.query(
                Favorite.id.label("id"),
                Favorite.date_created.label("date_created"),
                Book.id.label("book_id"),
                Book.title.label("title"),
                Author.name.label("author_name"),
                Category.name.label("category_name"),
                Book.published_year.label("published_year"),
            )
            .join(Book, Book.id == Favorite.book_id)
            .join(Author, Author.id == Book.author_id)
            .join(Category, Category.id == Book.category_id)
            .filter(
                Favorite.id == favorite.id,
                Favorite.user_id == user.id,
            )
            .first()
        )

    def remove_favorite(self, db: Session, user: User, book_id: int):
        favorite = self.get_favorite(db=db, user_id=user.id, book_id=book_id)
        db.delete(favorite)
        db.commit()
        return {"message": "Book removed from favorites."}

    def get_user_favorite_books(self, db: Session, user: User):
        return paginate(
            db.query(Favorite)
            .join(Book, Book.id == Favorite.book_id)
            .join(Category, Category.id == Book.category_id)
            .join(Author, Author.id == Book.author_id)
            .filter(Favorite.user_id == user.id)
            .with_entities(
                Favorite.id,
                Favorite.date_created,
                Book.id.label("book_id"),
                Book.title.label("title"),
                Author.name.label("author_name"),
                Category.name.label("category_name"),
                Book.published_year.label("published_year"),
            )
        )


favorite_core = FavoriteCore()
