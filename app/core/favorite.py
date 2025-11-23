from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.enums import Status
from app.helpers.error_helper import Error
from app.models import Book, Favorite, User
from app.models.author import Author
from app.models.category import Category


class FavoriteCore:
    def __init__(self) -> None:
        pass

    def get_favorite(self, db: Session, user_id: int, book_id: int):
        return (
            db.query(Favorite)
            .filter(
                Favorite.user_id == user_id,
                Favorite.book_id == book_id,
            )
            .first()
        )

    def add_favorite(self, db: Session, user: User, book_id: int) -> Favorite:
        # Kitap var mı ve aktif mi?
        book_core.get_book_by_id(db=db, book_id=book_id, only_active=True)

        # Favori mi?
        exists = self.get_favorite(db=db, user_id=user.id, book_id=book_id)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Error.favorite_already_exists,
            )

        favorite = Favorite(user_id=user.id, book_id=book_id)
        db.add(favorite)
        db.commit()
        return favorite

    def remove_favorite(self, db: Session, user: User, book_id: int):
        favorite = self.get_favorite(db=db, user_id=user.id, book_id=book_id)
        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Error.record_not_found,
            )

        db.delete(favorite)
        db.commit()
        return {"message": "Book removed from favorites."}

    def get_user_favorite_books_query(self, db: Session, user: User):
        return (
            db.query(Book)
            .join(Favorite, Favorite.book_id == Book.id)
            .join(Author, Author.id == Book.author_id)
            .join(Category, Category.id == Book.category_id)
            .filter(
                Favorite.user_id == user.id,
                Book.status == Status.active,
            )
            .with_entities(
                Book.id.label("id"),
                Book.date_created.label("date_created"),
                Book.title.label("title"),
                Author.name.label("author_name"),
                Category.name.label("category_name"),
                Book.published_year.label("published_year"),
            )
        )


favorite_core = FavoriteCore()
