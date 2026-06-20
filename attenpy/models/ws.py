from pydantic import BaseModel

from .notice import NoticeKind, NoticeType


class NoticeCreatedNotice(BaseModel):
    id: int
    user_id: int
    actor_id: int | None
    target_id: int | None
    additional_id: int | None
    type: NoticeType


class NoticeCreatedTarget(BaseModel):
    id: int
    kind: NoticeKind
    object_id: int | None
    content: str | None


class NoticeCreatedActor(BaseModel):
    id: int
    scratch_name: str | None
    display_name: str | None
    icon_id: int | None
    deleted: bool
