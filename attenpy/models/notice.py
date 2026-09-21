from datetime import datetime
from enum import StrEnum, auto
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..snowflake import Snowflake

if TYPE_CHECKING:
    from .user import PartialUser


class NoticeType(StrEnum):
    WELCOME = auto()
    LOGIN = auto()
    WARN = auto()
    FOLLOW = auto()
    MENTION = auto()
    REPLY = auto()
    QUOTE = auto()
    REPOST = auto()
    LOVE = auto()
    INVITE_CHAT = auto()
    ACCESS_REQUEST = auto()


class NoticeKind(StrEnum):
    SESSION = auto()
    POST = auto()
    CHAT = auto()
    WARN = auto()


class NoticeTarget(BaseModel):
    id: int
    kind: NoticeKind
    object_id: int
    content: str


class Notice(BaseModel):
    id: int
    user_id: int
    actor_id: int | None
    target_id: int | None
    additional_id: int | None
    type: NoticeType
    actor: "PartialUser | None"
    target: NoticeTarget | None
    is_read: bool

    def __int__(self) -> int:
        return self.id

    @property
    def created_at(self) -> datetime:
        return Snowflake(self.id).datetime
