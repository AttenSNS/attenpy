from collections.abc import AsyncGenerator
from types import EllipsisType
from typing import TYPE_CHECKING, Unpack

from ..models import (
    Attachment,
    Bot,
    PartialPost,
    PartialUser,
    Post,
    User,
    UserAccessStatus,
)
from ..pagination import PaginateOptions, paginate
from ..ref import UserRef
from ..utils import int_or_none

if TYPE_CHECKING:
    from ..client import Client


class MeEndpoint:
    def __init__(self, client: "Client"):
        self.client = client

    async def edit(
        self,
        *,
        display_name: str | None | EllipsisType = ...,
        bio: str | EllipsisType = ...,
        icon: int | Attachment | None | EllipsisType = ...,
        banner: int | Attachment | None | EllipsisType = ...,
        pinned: int | PartialPost | None | EllipsisType = ...,
    ) -> User:
        payload = {}
        if display_name is not ...:
            payload["display_name"] = display_name
        if bio is not ...:
            payload["bio"] = bio
        if icon is not ...:
            payload["icon_id"] = int_or_none(icon)
        if banner is not ...:
            payload["banner_id"] = int_or_none(banner)
        if pinned is not ...:
            payload["pinned_id"] = int_or_none(pinned)
        return User.model_validate(
            (await self.client.http.patch(f"/users/{UserRef.ME}", json=payload)).data
        )

    async def get_mutes(self, **kw: Unpack[PaginateOptions]) -> AsyncGenerator[PartialUser]:
        async for data in paginate(self.client.http, f"/users/{UserRef.ME}/mutes", **kw):
            yield PartialUser.model_validate(data)

    async def get_bookmarks(self, **kw: Unpack[PaginateOptions]) -> AsyncGenerator[Post]:
        async for data in paginate(self.client.http, f"/users/{UserRef.ME}/bookmarks", **kw):
            yield Post.model_validate(data)

    async def get_accesses(self, **kw: Unpack[PaginateOptions]) -> AsyncGenerator[PartialUser]:
        async for data in paginate(self.client.http, f"/users/{UserRef.ME}/accesses", **kw):
            yield PartialUser.model_validate(data)

    async def get_viewers(
        self,
        *,
        status: UserAccessStatus,
        **kw: Unpack[PaginateOptions],
    ) -> AsyncGenerator[PartialUser]:
        async for data in paginate(
            self.client.http,
            f"/users/{UserRef.ME}/viewers",
            params={"status": status.value},
            **kw,
        ):
            yield PartialUser.model_validate(data)

    async def accept_viewer(self, viewer: UserRef | str):
        await self.client.http.post(f"/users/{UserRef.ME}/viewers/{viewer}/accept")

    async def decline_viewer(self, viewer: UserRef | str):
        await self.client.http.post(f"/users/{UserRef.ME}/viewers/{viewer}/decline")

    async def remove_viewer(self, viewer: UserRef | str):
        await self.client.http.delete(f"/users/{UserRef.ME}/viewers/{viewer}")

    async def get_bot(self) -> Bot | None:
        data = (await self.client.http.get(f"/users/{UserRef.ME}/bot")).data
        return Bot.model_validate(data) if data is not None else None

    async def revoke_bot(self):
        await self.client.http.delete(f"/users/{UserRef.ME}/bot")
