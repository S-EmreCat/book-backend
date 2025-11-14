from pydantic import Field

from app.schemas.base import BaseSchema


class AdminLoginIn(BaseSchema):
    email: str = Field(example="sample@sample.com")
    password: str = Field(example="Admin1234")


class AdminLoginOut(BaseSchema):
    access_token: str


class ChangePasswordIn(BaseSchema):
    current_password: str = Field(..., example="Admin1234")
    new_password: str = Field(..., example="YeniSifre456")
