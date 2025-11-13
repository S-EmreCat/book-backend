from datetime import date

from pydantic import EmailStr, Field, field_validator

from app.schemas.base import BaseSchema


class RegisterIn(BaseSchema):
    first_name: str = Field(..., min_length=1, max_length=50, example="Name")
    last_name: str = Field(..., min_length=1, max_length=50, example="Lastname")
    email: EmailStr = Field(..., example="sample@sample.com")
    phone_number: str = Field(
        ...,
        example="+905321234567",
        description="+90 ile başlamalı ve toplam 13 karakter olmalı",
    )
    birth_date: date | None = Field(default=None, example="1995-01-01", description="Opsiyonel alan")
    password: str = Field(..., min_length=8, example="User1234", description="Minimum 8 karakter olmalı")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        if not v.startswith("+90"):
            raise ValueError("Telefon numarası +90 ile başlamalı.")

        if len(v) != 13 or not v[3:].isdigit():
            raise ValueError("Telefon numarası formatı hatalı. Örn: +905321234567")

        return v


class PanelLoginIn(BaseSchema):
    email: EmailStr = Field(..., example="sample@sample.com")
    password: str = Field(..., example="User1234")


class PanelLoginOut(BaseSchema):
    access_token: str
