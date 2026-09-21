from __future__ import annotations

from pydantic import BaseModel


class WsTokenPayload(BaseModel):
    token: str
