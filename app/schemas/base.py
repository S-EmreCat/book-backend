from enum import Enum

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        validate_by_name = True
        str_strip_whitespace = True
        json_encoders = {
            Enum: lambda g: g.name,
        }
