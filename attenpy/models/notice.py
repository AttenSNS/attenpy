from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..snowflake import Snowflake

if TYPE_CHECKING:
    from .user import PartialUser


class NoticeType(str, Enum):
    WELCOME = "welcome"
    LOGIN = "login"
    WARN = "warn"
    FOLLOW = "follow"
    MENTION = "mention"
    REPLY = "reply"
    QUOTE = "quote"
    REPOST = "repost"
    LOVE = "love"
    INVITE_CHAT = "invite_chat"


class NoticeKind(str, Enum):
    SESSION = "session"
    POST = "post"
    CHAT = "chat"
    WARN = "warn"


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
