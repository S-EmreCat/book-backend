from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import column_property, relationship

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

    login_histories = relationship("PanelUserLoginHistory", back_populates="panel_user", lazy="selectin")


class PanelUserLoginHistory(Base):
    __tablename__ = "panel_user_login_history"

    panel_user_id = Column(Integer, ForeignKey("panel_user.id"), nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)

    panel_user = relationship("PanelUser", back_populates="login_histories")


# TODO: panel_user_forget_pass_history
# TODO: panel_user_password_history
