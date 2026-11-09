from datetime import datetime

from pydantic import BaseModel


class Bot(BaseModel):
    id: int
    owner_user_id: int
    name: str
    generation: int
    created_at: datetime
    revoked_at: datetime | None
    is_revoked: bool

    def __int__(self) -> int:
        return self.id
