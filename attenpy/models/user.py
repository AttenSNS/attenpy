from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .attachment import Attachment, ExternalAttachment


class PartialUser(BaseModel):
    id: int
    scratch_name: str
    display_name: str
    icon: "Attachment | ExternalAttachment"
    public_flags: int  # TODO
    deleted: bool
    is_muted: bool
    is_following: bool | None = None
    is_followed: bool | None = None


class User(PartialUser):
    # pinned
    followers_count: int
    following_count: int
    post_count: int
    love_count: int
