from enum import Enum

from app.enums.base_enum import BaseEnum


class Status(int, BaseEnum):
    active = 1
    passive = 0
    deleted = -1


class StatusInput(int, BaseEnum):
    active = 1
    passive = 0


class CommentStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    deleted = "deleted"


class CommentStatusInput(str, Enum):
    approved = "approved"
    rejected = "rejected"


class CommentRejectionReason(str, Enum):
    spam = "SPAM"
    offensive = "OFFENSIVE"
    irrelevant = "IRRELEVANT"
    other = "OTHER"
