from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums import Status
from app.helpers.error_helper import Error
from app.models import Author
from app.schemas.admin.author import AuthorIn


class AuthorCore:
    def __init__(self):
        pass

    def get_author_by_id(self, db: Session, author_id: int, only_active=True):
        filters = [Author.id == author_id, Author.status != Status.deleted]
        if only_active:
            filters.append(Author.status == Status.active)
        author = db.query(Author).filter(*filters).first()
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=Error.author_not_found,
            )
        return author

    def get_all_authors(self, db: Session, status=None):
        filters = []
        if status is not None:
            filters.append(Author.status == status)
        else:
            filters.append(Author.status != Status.deleted)
        return db.query(Author).filter(*filters).all()

    def create_author(self, db: Session, data: AuthorIn):
        # Aynı isimde kayıt varsa hata verelim
        existing = db.query(Author).filter(Author.name == data.name, Author.status != Status.deleted).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Error.author_already_exists,
            )

        author = Author(
            name=data.name,
            description=data.description,
            image_url=data.image_url,
            status=data.status,
        )
        db.add(author)
        db.commit()
        return author

    def update_author(self, db: Session, author_id: int, data: AuthorIn):
        author = self.get_author_by_id(db=db, author_id=author_id, only_active=False)

        # İsim değişikliği durumunda da aynı isim kontrolü yapılabilir (isteğe bağlı)
        if data.name != author.name:
            existing = (
                db.query(Author)
                .filter(
                    Author.name == data.name,
                    Author.id != author_id,
                    Author.status != Status.deleted,
                )
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=Error.author_already_exists,
                )

        author.name = data.name
        author.description = data.description
        author.image_url = data.image_url
        author.status = data.status
        db.commit()
        return author

    def delete_author(self, db: Session, author_id: int):
        author = self.get_author_by_id(db=db, author_id=author_id, only_active=False)
        author.status = Status.deleted
        db.commit()
        return {"message": "Author deleted successfully."}


author_core = AuthorCore()
