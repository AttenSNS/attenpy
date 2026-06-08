from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .attachment import Attachment
    from .user import PartialUser


class PartialPost(BaseModel):
    id: str
    author_id: str
    author: "PartialUser"
    content_md: str
    parent_id: str | None
    target_history_id: str | None
    current_history_id: str
    quote_id: str | None
    root_id: str | None
    is_repost: bool
    is_edited: bool
    deleted: bool
    attachments: list["Attachment"]


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
