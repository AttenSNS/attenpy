from collections.abc import AsyncGenerator, Sequence
from datetime import datetime
from typing import TYPE_CHECKING, Unpack

from pydantic import TypeAdapter

from attenpy import UserRef

from ..models import Post, PostVisibility
from ..pagination import (
    PaginateOptions,
    paginate,
)
from ..payloads import TrendPayload
from ..utils import api_bool

if TYPE_CHECKING:
    from ..client import Client

TREND_DATA_TA = TypeAdapter[list[TrendPayload]](list[TrendPayload])


class ExploreEndpoint:
    def __init__(self, client: "Client"):
        self.client = client

    async def get_recent(self, **kw: Unpack[PaginateOptions]) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, "/explore/recent", **kw):
            yield Post.model_validate(data)

    async def get_following_post(self, **kw: Unpack[PaginateOptions]) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, "/explore/following", **kw):
            yield Post.model_validate(data)

    async def get_mix_post(self, **kw: Unpack[PaginateOptions]) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, "/explore/mix", **kw):
            yield Post.model_validate(data)

    async def get_trend(self) -> AsyncGenerator[TrendPayload]:
        for data in TREND_DATA_TA.validate_python(
            (await self.client.http.post("/explore/trend")).data
        ):
            yield data

    async def search_post(
        self,
        q: str,
        *,
        user: Sequence[UserRef | str] | None = None,
        visibility: PostVisibility | None = None,
        is_reply: bool | None = None,
        before: datetime | str | None = None,
        after: datetime | str | None = None,
        **kw: Unpack[PaginateOptions],
    ) -> AsyncGenerator[Post]:
        params = dict[str, str | list[str]](q=q)
        if user:
            params["user"] = list(map(str, user))
        if visibility:
            params["visibility"] = str(visibility)
        if is_reply is not None:
            params["is_reply"] = api_bool(is_reply)
        if before:
            params["before"] = before.isoformat() if isinstance(before, datetime) else str(before)
        if after:
            params["after"] = after.isoformat() if isinstance(after, datetime) else str(after)
        async for data in paginate(self.client.http, "/explore/search", params=params, **kw):
            yield Post.model_validate(data)
