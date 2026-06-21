from __future__ import annotations

from pydantic import BaseModel


class WsTokenPayload(BaseModel):
    token: str


class BotReadyPayload(BaseModel):
    bot_id: int
    owner_user_id: int
