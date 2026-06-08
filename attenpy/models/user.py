from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .attachment import Attachment, ExternalAttachment
    from .post import Post


class PartialUser(BaseModel):
    id: int
    scratch_name: str
    display_name: str | None
    icon: "Attachment | ExternalAttachment"
    public_flags: int  # TODO
    deleted: bool
    is_muted: bool | None
    is_following: bool | None = None
    is_followed: bool | None = None


class User(PartialUser):
    scratch_id: int
    bio: str
    pinned: "Post | None"
    followers_count: int
    following_count: int
    post_count: int
    love_count: int
