from datetime import datetime

from pydantic import BaseModel

from attenpy.models import Warn


class BanStatusPayload(BaseModel):
    is_banned: bool
    banned_at: datetime | None
    unbanned_at: datetime | None
    ban_warn: Warn | None
    recent_warns: list[Warn]
