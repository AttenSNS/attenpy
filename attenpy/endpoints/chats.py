from collections.abc import AsyncGenerator, Sequence
from typing import TYPE_CHECKING, Unpack

from ..models import Attachment, ChatChannel, ChatMember, ChatMessage, PartialChatMessage
from ..pagination import PaginateOptions, paginate
from ..payloads import ChatUnreadCountPayload
from ..ref import UserRef
from ..utils import int_or_none

if TYPE_CHECKING:
    from ..client import Client


class ChatEndpoint:
    def __init__(self, client: "Client"):
        self.client = client

    async def list(self, **kw: Unpack[PaginateOptions]) -> AsyncGenerator[ChatChannel]:
        async for data in paginate(self.client.http, "/chats", **kw):
            yield ChatChannel.model_validate(data)

    async def get_unread_count(self) -> ChatUnreadCountPayload:
        return ChatUnreadCountPayload.model_validate(
            (await self.client.http.get("/chats/unread-count")).data
        )

    async def get(self, channel: int | ChatChannel) -> ChatChannel:
        return ChatChannel.model_validate(
            (await self.client.http.get(f"/chats/{int(channel)}")).data
        )

    async def get_members(
        self, channel: int | ChatChannel, **kw: Unpack[PaginateOptions]
    ) -> AsyncGenerator[ChatMember]:
        async for data in paginate(self.client.http, f"/chats/{int(channel)}/members", **kw):
            yield ChatMember.model_validate(data)

    async def get_member(self, channel: int | ChatChannel, user: UserRef | str) -> ChatMember:
        return ChatMember.model_validate(
            (await self.client.http.get(f"/chats/{int(channel)}/members/{user}")).data
        )

    async def join(self, channel: int | ChatChannel) -> ChatChannel:
        return ChatChannel.model_validate(
            (
                await self.client.http.patch(
                    f"/chats/{int(channel)}/members/{UserRef.ME}", json={"is_joined": True}
                )
            ).data
        )

    async def remove_member(self, channel: int | ChatChannel, user: UserRef | str):
        await self.client.http.delete(f"/chats/{int(channel)}/members/{user}")

    async def mark_read(self, channel: int | ChatChannel):
        await self.client.http.post(f"/chats/{int(channel)}/read")

    async def create_message(
        self,
        channel: int | ChatChannel,
        content: str = "",
        *,
        attachments: Sequence[int | Attachment] | None = None,
        reply: int | PartialChatMessage | None = None,
    ) -> ChatMessage:
        return ChatMessage.model_validate(
            (
                await self.client.http.post(
                    f"/chats/{int(channel)}/messages",
                    json={
                        "content": content,
                        "attachment_ids": [int(attachment) for attachment in attachments or []],
                        "reply_id": int_or_none(reply),
                    },
                )
            ).data
        )

    async def get_messages(
        self, channel: int | ChatChannel, **kw: Unpack[PaginateOptions]
    ) -> AsyncGenerator[ChatMessage]:
        async for data in paginate(self.client.http, f"/chats/{int(channel)}/messages", **kw):
            yield ChatMessage.model_validate(data)
