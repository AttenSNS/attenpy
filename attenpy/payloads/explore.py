from pydantic import BaseModel


class TrendPayload(BaseModel):
    tag: str
    user_count: int
    post_count: int
