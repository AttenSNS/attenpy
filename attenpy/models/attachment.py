from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from ..snowflake import Snowflake


class PartialAttachment(BaseModel):
    url: str


class Attachment(BaseModel):
    id: int
    url: str
    category: Literal[
        "icon", "banner", "post_attachment", "group_icon", "chat_attachment"
    ]
    mime: str
    deleted: bool

    def __int__(self) -> int:
        return self.id

    @property
    def created_at(self) -> datetime:
        return Snowflake(self.id).datetime
