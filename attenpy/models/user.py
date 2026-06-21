from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..ref import UserRef
from ..snowflake import Snowflake

if TYPE_CHECKING:
    from .attachment import Attachment, PartialAttachment
    from .post import Post


class PartialUser(BaseModel):
    id: int
    scratch_name: str
    display_name: str | None
    icon: "Attachment | PartialAttachment"
    public_flags: int  # TODO
    deleted: bool
    is_muted: bool | None
    is_following: bool | None = None
    is_followed: bool | None = None

    def __int__(self) -> int:
        return self.id

    @property
    def ref(self):
        return UserRef(user_id=self.id)

    @property
    def created_at(self) -> datetime:
        return Snowflake(self.id).datetime


class User(PartialUser):
    scratch_id: int
    bio: str
    pinned: "Post | None"
    followers_count: int
    following_count: int
    post_count: int
    love_count: int
