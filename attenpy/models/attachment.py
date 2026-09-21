from datetime import datetime
from enum import StrEnum, auto

from pydantic import BaseModel

from ..snowflake import Snowflake


class AttachmentCategory(StrEnum):
    ICON = auto()
    BANNER = auto()
    POST_ATTACHMENT = auto()
    GROUP_ICON = auto()
    CHAT_ATTACHMENT = auto()


class PartialAttachment(BaseModel):
    url: str


class Attachment(BaseModel):
    id: int
    url: str
    category: AttachmentCategory
    mime: str
    deleted: bool

    def __int__(self) -> int:
        return self.id

    @property
    def created_at(self) -> datetime:
        return Snowflake(self.id).datetime
