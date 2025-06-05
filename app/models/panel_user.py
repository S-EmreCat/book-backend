from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import column_property

from app.enums import Status
from app.models.base import Base


class PanelUser(Base):
    __tablename__ = "panel_user"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = column_property(first_name + " " + last_name)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    password_hash = Column(String(120), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.active)


# TODO: panel_user_login_history
# TODO: panel_user_forget_pass_history
# TODO: panel_user_password_history
