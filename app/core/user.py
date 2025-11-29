from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.enums import Status
from app.helpers.error_helper import Error
from app.helpers.hash_helper import hash_helper
from app.models import User
from app.schemas.panel.auth import RegisterIn
from app.schemas.panel.user import UserMeUpdateIn


class UserCore:
    def __init__(self) -> None:
        pass

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email, User.status != Status.deleted).first()

    def get_user_by_phone(self, db: Session, phone_number: str) -> Optional[User]:
        return db.query(User).filter(User.phone_number == phone_number, User.status != Status.deleted).first()

    def create_user(self, db: Session, data: RegisterIn) -> User:
        # email uniq kontrolü
        if self.get_user_by_email(db=db, email=data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=Error.user_email_exists,
            )

        # phone uniq kontrolü
        if self.get_user_by_phone(db=db, phone_number=data.phone_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=Error.user_phone_exists,
            )

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            phone_number=data.phone_number,
            email=data.email,
            birth_date=data.birth_date,
            password_hash=hash_helper.get_password_hash(data.password),
            status=Status.active,
        )
        db.add(user)
        db.commit()
        return user

    def authenticate_user(self, db: Session, email: str, password: str) -> User:
        user = self.get_user_by_email(db=db, email=email)

        if not user or not hash_helper.verify(user.password_hash, password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Error.invalid_user_credentials,
            )

        if user.status != Status.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Error.user_not_active,
            )

        return user

    def update_me(
        self,
        db: Session,
        user: User,
        data: UserMeUpdateIn,
    ):
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.birth_date = data.birth_date
        db.commit()

        return user


user_core = UserCore()
