from __future__ import annotations

from pydantic import BaseModel

from ..models import (
    NoticeCreatedActor,
    NoticeCreatedNotice,
    NoticeCreatedTarget,
)


class WsTokenPayload(BaseModel):
    token: str


class BotReadyPayload(BaseModel):
    bot_id: int
    owner_user_id: int


class NoticeCreatedPayload(BaseModel):
    notice: NoticeCreatedNotice
    target: NoticeCreatedTarget | None
    actor: NoticeCreatedActor | None
