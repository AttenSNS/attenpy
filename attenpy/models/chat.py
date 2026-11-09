from datetime import datetime
from enum import StrEnum, auto
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..snowflake import Snowflake

if TYPE_CHECKING:
    from .attachment import Attachment
    from .user import PartialUser


class ChatMessageType(StrEnum):
    MESSAGE = auto()
    INVITED = auto()
    JOINED = auto()
    LEFT = auto()
    KICKED = auto()
    TRANSFERRED = auto()
    DELETED = auto()
    WARN = auto()


class PartialChatMessage(BaseModel):
    id: int
    channel_id: int
    type: ChatMessageType
    content: str
    edited_at: datetime | None
    author: "PartialUser"
    attachments: list["Attachment"]

    def __int__(self) -> int:
        return self.id

    @property
    def created_at(self) -> datetime:
        return Snowflake(self.id).created_at


class ChatMessage(PartialChatMessage):
    target_message: PartialChatMessage | None
    target_user: "PartialUser | None"
    is_read: bool


class ChatChannel(BaseModel):
    id: int
    title: str
    is_group: bool
    everyone_can_invite: bool
    member_count: int
    owner_id: int | None
    icon: "Attachment | None"
    is_joined: bool
    read_message_id: int
    unread_message_count: int
    newest_message: PartialChatMessage | None
    partner: "PartialUser | None"

    def __int__(self) -> int:
        return self.id

    @property
    def created_at(self) -> datetime:
        return Snowflake(self.id).created_at


class ChatMember(BaseModel):
    user: "PartialUser"
    is_joined: bool
    is_owner: bool
