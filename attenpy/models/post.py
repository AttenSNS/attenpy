from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..snowflake import Snowflake

if TYPE_CHECKING:
    from .attachment import Attachment
    from .user import PartialUser


class PartialPost(BaseModel):
    id: int
    author_id: str
    author: "PartialUser"
    content_md: str
    parent_id: int | None
    target_history_id: int | None
    current_history_id: int
    quote_id: str | None
    root_id: str | None
    is_repost: bool
    is_edited: bool
    deleted: bool
    attachments: list["Attachment"]

    def __int__(self) -> int:
        return self.id

    @property
    def created_at(self) -> datetime:
        return Snowflake(self.id).datetime


class Post(PartialPost):
    parent: PartialPost | None
    quote: PartialPost | None
    love_count: int
    bookmark_count: int
    reply_count: int
    quote_count: int
    is_loved: bool | None
    is_bookmarked: bool | None
    is_reposted: bool | None
    target: "Post | None" = None
    version: int | None = None
    is_latest: bool = True
