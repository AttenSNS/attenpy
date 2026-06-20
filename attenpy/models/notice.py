from datetime import datetime
from typing import TYPE_CHECKING, Literal, TypeAlias

from pydantic import BaseModel

from ..snowflake import Snowflake

if TYPE_CHECKING:
    from .user import PartialUser

NoticeType: TypeAlias = Literal[
    "welcome",
    "login",
    "warn",
    "follow",
    "mention",
    "reply",
    "quote",
    "repost",
    "love",
    "invite_chat",
]

NoticeKind: TypeAlias = Literal["session", "post", "chat", "warn"]


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
