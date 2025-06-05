from datetime import datetime

from sqlalchemy import Column, DateTime, Integer

from app.database.database import sBase


class Base(sBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.now)
    date_modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
