from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Unpack

from attenpy.payloads import BanStatusPayload

from ..models import ChatChannel, PartialUser, Post, User
from ..pagination import (
    PaginateOptions,
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
        self, user: UserRef | str, **kw: Unpack[PaginateOptions]
    ) -> AsyncGenerator[PartialUser]:
        async for data in paginate(self.client.http, f"/users/{user}/followers", **kw):
            yield PartialUser.model_validate(data)

    async def get_following(
        self, user: UserRef | str, **kw: Unpack[PaginateOptions]
    ) -> AsyncGenerator[PartialUser]:
        async for data in paginate(self.client.http, f"/users/{user}/following", **kw):
            yield PartialUser.model_validate(data)

    async def get_posts(
        self, user: UserRef | str, **kw: Unpack[PaginateOptions]
    ) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, f"/users/{user}/posts", **kw):
            yield Post.model_validate(data)

    async def get_medias(
        self, user: UserRef | str, **kw: Unpack[PaginateOptions]
    ) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, f"/users/{user}/medias", **kw):
            yield Post.model_validate(data)

    async def get_loves(
        self, user: UserRef | str, **kw: Unpack[PaginateOptions]
    ) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, f"/users/{user}/loves", **kw):
            yield Post.model_validate(data)

    async def get_reposts(
        self, user: UserRef | str, **kw: Unpack[PaginateOptions]
    ) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, f"/users/{user}/reposts", **kw):
            yield Post.model_validate(data)

    async def ban_status(self, user: UserRef | str) -> BanStatusPayload:
        return BanStatusPayload.model_validate(
            (await self.client.http.get(f"/users/{user}/ban")).data
        )

    async def request_access(self, user: UserRef | str):
        await self.client.http.post(f"/users/{user}/access")

    async def remove_access(self, user: UserRef | str):
        await self.client.http.delete(f"/users/{user}/access")

    async def get_chat(self, user: UserRef | str) -> ChatChannel:
        return ChatChannel.model_validate((await self.client.http.get(f"/users/{user}/chat")).data)
