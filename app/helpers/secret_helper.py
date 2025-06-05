from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, status

from app.config import settings


class SecretHelper:
    def __init__(self):
        pass

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_jwt_encode = data.copy()

        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=settings.JWT_EXPIRES_TIME)

        to_jwt_encode.update({"exp": expire})
        return jwt.encode(to_jwt_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        try:
            data = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                verify=True,
            )
            if data is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return data
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def get_expire_date(second: int):
        return datetime.now() + timedelta(seconds=second)


secret_helper = SecretHelper()
