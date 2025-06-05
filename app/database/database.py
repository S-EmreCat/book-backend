from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args=settings.SQLALCHEMY_CONNECT_ARGS,
    max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
    pool_recycle=settings.SQLALCHEMY_POOL_RECYCLE,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    pool_timeout=settings.SQLALCHEMY_POOL_TIMEOUT,
    echo=settings.SQLALCHEMY_ECHO,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


sBase = declarative_base()
