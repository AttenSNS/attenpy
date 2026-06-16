from pydantic import BaseModel


class NoticeUnreadCountPayload(BaseModel):
    unread_count: int
    last_read_notice_id: int
