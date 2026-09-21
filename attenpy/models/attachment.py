from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

from ..snowflake import Snowflake


class AttachmentCategory(StrEnum):
    ICON = "icon"
    BANNER = "banner"
    POST_ATTACHMENT = "post_attachment"
    GROUP_ICON = "group_icon"
    CHAT_ATTACHMENT = "chat_attachment"


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
