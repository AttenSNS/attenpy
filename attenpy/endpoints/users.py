from typing import TYPE_CHECKING, AsyncIterator

from ..models import PartialUser, Post, User
from ..pagination import (
    MAX_PAGINATION_LIMIT,
    PAGINATE_ORDER,
    PAGINATE_ORDER_DEFAULT,
    paginate,
)
from ..ref import UserRef

if TYPE_CHECKING:
    from ..client import Client


class UserEndpoint:
    def __init__(self, client: "Client"):
        self.client = client

    async def get(self, user: UserRef | str) -> User:
        return User.model_validate((await self.client.http.get(f"/users/{user}")).data)

    async def follow(self, user: UserRef | str):
        await self.client.http.post(f"/users/{user}/follow")

    async def unfollow(self, user: UserRef | str):
        await self.client.http.delete(f"/users/{user}/follow")

    async def mute(self, user: UserRef | str):
        await self.client.http.post(f"/users/{user}/mute")

    async def unmute(self, user: UserRef | str):
        await self.client.http.delete(f"/users/{user}/mute")

    async def get_followers(
        self,
        user: UserRef | str,
        *,
        limit: int = MAX_PAGINATION_LIMIT,
        cursor: int | None = None,
        order: PAGINATE_ORDER = PAGINATE_ORDER_DEFAULT,
    ) -> AsyncIterator[PartialUser]:
        async for data in paginate(
            self.client.http,
            f"/users/{user}/followers",
            cursor=cursor,
            limit=limit,
            order=order,
        ):
            yield PartialUser.model_validate(data)

    async def get_following(
        self,
        user: UserRef | str,
        *,
        limit: int = MAX_PAGINATION_LIMIT,
        cursor: int | None = None,
        order: PAGINATE_ORDER = PAGINATE_ORDER_DEFAULT,
    ) -> AsyncIterator[PartialUser]:
        async for data in paginate(
            self.client.http,
            f"/users/{user}/following",
            cursor=cursor,
            limit=limit,
            order=order,
        ):
            yield PartialUser.model_validate(data)

    async def get_mutes(
        self,
        user: UserRef | str,
        *,
        limit: int = MAX_PAGINATION_LIMIT,
        cursor: int | None = None,
        order: PAGINATE_ORDER = PAGINATE_ORDER_DEFAULT,
    ) -> AsyncIterator[PartialUser]:
        async for data in paginate(
            self.client.http,
            f"/users/{user}/mutes",
            cursor=cursor,
            limit=limit,
            order=order,
        ):
            yield PartialUser.model_validate(data)

    async def get_posts(
        self,
        user: UserRef | str,
        *,
        limit: int = MAX_PAGINATION_LIMIT,
        cursor: int | None = None,
        order: PAGINATE_ORDER = PAGINATE_ORDER_DEFAULT,
    ) -> AsyncIterator[Post]:
        async for data in paginate(
            self.client.http,
            f"/users/{user}/posts",
            cursor=cursor,
            limit=limit,
            order=order,
        ):
            yield Post.model_validate(data)

    async def get_medias(
        self,
        user: UserRef | str,
        *,
        limit: int = MAX_PAGINATION_LIMIT,
        cursor: int | None = None,
        order: PAGINATE_ORDER = PAGINATE_ORDER_DEFAULT,
    ) -> AsyncIterator[Post]:
        async for data in paginate(
            self.client.http,
            f"/users/{user}/medias",
            cursor=cursor,
            limit=limit,
            order=order,
        ):
            yield Post.model_validate(data)

    async def get_loves(
        self,
        user: UserRef | str,
        *,
        limit: int = MAX_PAGINATION_LIMIT,
        cursor: int | None = None,
        order: PAGINATE_ORDER = PAGINATE_ORDER_DEFAULT,
    ) -> AsyncIterator[Post]:
        async for data in paginate(
            self.client.http,
            f"/users/{user}/loves",
            cursor=cursor,
            limit=limit,
            order=order,
        ):
            yield Post.model_validate(data)

    async def get_bookmarks(
        self,
        user: UserRef | str,
        *,
        limit: int = MAX_PAGINATION_LIMIT,
        cursor: int | None = None,
        order: PAGINATE_ORDER = PAGINATE_ORDER_DEFAULT,
    ) -> AsyncIterator[Post]:
        async for data in paginate(
            self.client.http,
            f"/users/{user}/bookmarks",
            cursor=cursor,
            limit=limit,
            order=order,
        ):
            yield Post.model_validate(data)

    async def get_reposts(
        self,
        user: UserRef | str,
        *,
        limit: int = MAX_PAGINATION_LIMIT,
        cursor: int | None = None,
        order: PAGINATE_ORDER = PAGINATE_ORDER_DEFAULT,
    ) -> AsyncIterator[Post]:
        async for data in paginate(
            self.client.http,
            f"/users/{user}/reposts",
            cursor=cursor,
            limit=limit,
            order=order,
        ):
            yield Post.model_validate(data)
