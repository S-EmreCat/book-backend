import os

from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    # MYSQL
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_ROOT_PASSWORD: str = os.getenv("MYSQL_ROOT_PASSWORD", "root1234")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "book-db")
    SQLALCHEMY_DATABASE_URI: str = (
        f"mysql://{MYSQL_USER}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8"
    )

    # SQLALCHEMY SETTINGS
    SQLALCHEMY_CONNECT_ARGS: dict = {"charset": "utf8mb4", "connect_timeout": 10}
    SQLALCHEMY_MAX_OVERFLOW: int = 12
    SQLALCHEMY_POOL_RECYCLE: int = 1800
    SQLALCHEMY_POOL_SIZE: int = 6
    SQLALCHEMY_POOL_TIMEOUT: int = 10
    SQLALCHEMY_ECHO: bool = False

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_TIME: int = 15  # minutes
    JWT_SECRET_KEY: str = "59f9fdd8aad6c594c4d12a1c8ce6690ae9e5ecee79a967d75eab0bdf53edc55e=="


settings = DefaultSettings()
