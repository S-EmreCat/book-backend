from sqlalchemy import Boolean, Column, Date, Enum, String
from sqlalchemy.orm import column_property, relationship

from app.enums import Status
from app.models.base import Base


class User(Base):
    __tablename__ = "user"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = column_property(first_name + " " + last_name)
    phone_number = Column(String(15), nullable=False)
    email = Column(String(50), nullable=False)
    birth_date = Column(Date)

    email_verification = Column(Boolean, nullable=False, default=False)
    phone_verification = Column(Boolean, nullable=False, default=False)

    password_hash = Column(String(120), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.active)

    favorites = relationship("Favorite", back_populates="user", lazy="selectin")


# TODO: table: user_login_history
# TODO: table: user_forget_pass_history
# TODO: table: user_password_history
