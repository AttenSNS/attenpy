from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Unpack

from pydantic import TypeAdapter

from ..models import Post
from ..pagination import PaginateOptions, paginate
from ..payloads import StatPayload, TrendPayload

if TYPE_CHECKING:
    from ..client import Client

TREND_DATA_TA = TypeAdapter[list[TrendPayload]](list[TrendPayload])
STAT_DATA_TA = TypeAdapter[list[StatPayload]](list[StatPayload])
MIX_DATA_TA = TypeAdapter[list[Post]](list[Post])


class ExploreEndpoint:
    def __init__(self, client: "Client"):
        self.client = client

    async def get_recent(self, **kw: Unpack[PaginateOptions]) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, "/explore/recent", **kw):
            yield Post.model_validate(data)

    async def get_following_post(self, **kw: Unpack[PaginateOptions]) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, "/explore/following", **kw):
            yield Post.model_validate(data)

    async def get_mix_post(self) -> AsyncGenerator[Post]:
        for data in MIX_DATA_TA.validate_python((await self.client.http.get("/explore/mix")).data):
            yield data

    async def get_trend(self) -> AsyncGenerator[TrendPayload]:
        for data in TREND_DATA_TA.validate_python(
            (await self.client.http.get("/explore/trend")).data
        ):
            yield data

    async def get_stats(self) -> AsyncGenerator[StatPayload]:
        for data in STAT_DATA_TA.validate_python((await self.client.http.get("/stats")).data):
            yield data
