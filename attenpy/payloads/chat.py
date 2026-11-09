from pydantic import BaseModel


class ChatUnreadCountPayload(BaseModel):
    unread_count: int
