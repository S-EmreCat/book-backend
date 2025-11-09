from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base  # id, date_created, date_modified, status vs. buradan geliyor


class PanelUserLoginHistory(Base):
    __tablename__ = "panel_user_login_history"

    panel_user_id = Column(Integer, ForeignKey("panel_user.id"), nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)

    panel_user = relationship("PanelUser", back_populates="login_histories")
