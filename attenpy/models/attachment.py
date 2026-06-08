from typing import Literal

from pydantic import BaseModel


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


class ExternalAttachment(BaseModel):
    url: str
