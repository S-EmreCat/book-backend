from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    # MYSQL
    MYSQL_USER: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DATABASE: str

    # SQLAlchemy URI
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"mysql://{self.MYSQL_USER}:{self.MYSQL_ROOT_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8"
        )

    # SQLALCHEMY SETTINGS
    SQLALCHEMY_CONNECT_ARGS: dict = {"charset": "utf8mb4", "connect_timeout": 10}
    SQLALCHEMY_MAX_OVERFLOW: int = 12
    SQLALCHEMY_POOL_RECYCLE: int = 1800
    SQLALCHEMY_POOL_SIZE: int = 6
    SQLALCHEMY_POOL_TIMEOUT: int = 10
    SQLALCHEMY_ECHO: bool = False

    # JWT
    JWT_ALGORITHM: str
    JWT_EXPIRES_TIME: int
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = DefaultSettings()
