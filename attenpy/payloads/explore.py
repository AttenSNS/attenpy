from datetime import date

from pydantic import BaseModel


class TrendPayload(BaseModel):
    tag: str
    user_count: int
    post_count: int


class StatPayload(BaseModel):
    date: date
    total_posts: int
    total_replies: int
    total_loves: int
    total_reposts: int
    total_users: int
    total_notices: int
    total_chat_channels: int
    total_chat_messages: int
    total_requests: int
