from typing import TYPE_CHECKING, AsyncIterator, Unpack

from ..models import PartialPost, PartialUser, Post
from ..pagination import (
    PaginateOptions,
    paginate,
)
from ..payloads import ParentsPostPayload
from ..utils import int_or_none

if TYPE_CHECKING:
    from ..client import Client


class PostEndpoint:
    def __init__(self, client: "Client"):
        self.client = client

    async def create(
        self,
        content: str,
        quote: int | PartialPost | None = None,
    ) -> Post:
        return Post.model_validate(
            (
                await self.client.http.post(
                    "/posts", json={"content": content, "quote": int_or_none(quote)}
                )
            ).data
        )

    async def get(self, post: int | PartialPost) -> Post:
        return Post.model_validate(
            (await self.client.http.get(f"/posts/{int(post)}")).data
        )

    async def reply(
        self,
        parent: int | PartialPost,
        content: str,
        quote: int | PartialPost | None = None,
    ) -> Post:
        return Post.model_validate(
            (
                await self.client.http.post(
                    f"/posts/{int(parent)}/reply",
                    json={"content": content, "quote": int_or_none(quote)},
                )
            ).data
        )

    async def delete(self, post: int | PartialPost):
        await self.client.http.delete(f"/posts/{int(post)}")

    async def love(self, post: int | PartialPost):
        await self.client.http.post(f"/posts/{int(post)}/love")

    async def unlove(self, post: int | PartialPost):
        await self.client.http.delete(f"/posts/{int(post)}/love")

    async def bookmark(self, post: int | PartialPost):
        await self.client.http.post(f"/posts/{int(post)}/bookmark")

    async def unbookmark(self, post: int | PartialPost):
        await self.client.http.delete(f"/posts/{int(post)}/bookmark")

    async def repost(self, post: int | PartialPost) -> Post:
        return Post.model_validate(
            (await self.client.http.post(f"/posts/{int(post)}/repost")).data
        )

    async def unrepost(self, post: int | PartialPost):
        await self.client.http.delete(f"/posts/{int(post)}/repost")

    async def get_loves(
        self, post: int | PartialPost, **kw: Unpack[PaginateOptions]
    ) -> AsyncIterator[PartialUser]:
        async for data in paginate(self.client.http, f"/posts/{int(post)}/loves", **kw):
            yield PartialUser.model_validate(data)

    async def get_history(
        self, post: int | PartialPost, **kw: Unpack[PaginateOptions]
    ) -> AsyncIterator[Post]:
        async for data in paginate(
            self.client.http, f"/posts/{int(post)}/history", **kw
        ):
            yield Post.model_validate(data)

    async def get_quotes(
        self, post: int | PartialPost, **kw: Unpack[PaginateOptions]
    ) -> AsyncIterator[Post]:
        async for data in paginate(
            self.client.http, f"/posts/{int(post)}/quotes", **kw
        ):
            yield Post.model_validate(data)

    async def get_replies(
        self, post: int | PartialPost, **kw: Unpack[PaginateOptions]
    ) -> AsyncIterator[Post]:
        async for data in paginate(
            self.client.http, f"/posts/{int(post)}/replies", **kw
        ):
            yield Post.model_validate(data)

    async def get_reposts(
        self, post: int | PartialPost, **kw: Unpack[PaginateOptions]
    ) -> AsyncIterator[Post]:
        async for data in paginate(
            self.client.http, f"/posts/{int(post)}/reposts", **kw
        ):
            yield Post.model_validate(data)

    async def get_parents(self, post: int | PartialPost) -> ParentsPostPayload:
        return ParentsPostPayload.model_validate(
            (await self.client.http.get(f"/posts/{int(post)}/parents")).data
        )
