from typing import Literal

from pydantic import BaseModel


class Attachment(BaseModel):
    id: str
    url: str
    category: Literal[
        "icon", "banner", "post_attachment", "group_icon", "chat_attachment"
    ]
    mime: str
    deleted: bool


class ExternalAttachment(BaseModel):
    url: str
