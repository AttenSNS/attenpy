from pydantic import BaseModel

from ..models import Post


class ParentsPostPayload(BaseModel):
    root: Post | None
    parents: list[Post]
    next_id: int | None
