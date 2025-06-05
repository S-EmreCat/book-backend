from enum import Enum
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class BaseEnum(Enum):
    @classmethod
    def _validate(cls, v: str, _: core_schema.ValidationInfo) -> Enum:
        if isinstance(v, Enum):
            return v
        try:
            _ = cls.lookup[v]
            return cls[v]
        except KeyError:
            permitted = ", ".join(v for v in cls.keys)
            raise ValueError(f"value is not a valid enumeration member; permitted: {permitted}")

    @classmethod
    def __get_pydantic_core_schema__(cls, _: type[Any], __: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        cls.lookup = {v: k.value for v, k in cls.__members__.items()}
        cls.keys = [*cls.lookup]
        return core_schema.with_info_before_validator_function(
            cls._validate,
            core_schema.any_schema(),
        )
