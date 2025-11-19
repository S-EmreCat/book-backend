from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import column_property, relationship

from app.enums import Status
from app.models.base import Base


class AdminUser(Base):
    __tablename__ = "admin_user"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = column_property(first_name + " " + last_name)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    password_hash = Column(String(120), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.active)

    login_histories = relationship("AdminUserLoginHistory", back_populates="admin_user", lazy="selectin")


class AdminUserLoginHistory(Base):
    __tablename__ = "admin_user_login_history"

    admin_user_id = Column(Integer, ForeignKey("admin_user.id"), nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)

    admin_user = relationship("AdminUser", back_populates="login_histories")


# TODO: admin_user_forget_pass_history
# TODO: admin_user_password_history
