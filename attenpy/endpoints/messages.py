from typing import TYPE_CHECKING

from ..models import ChatMessage

if TYPE_CHECKING:
    from ..client import Client


class MessageEndpoint:
    def __init__(self, client: "Client"):
        self.client = client

    async def get(self, message: int | ChatMessage) -> ChatMessage:
        return ChatMessage.model_validate(
            (await self.client.http.get(f"/messages/{int(message)}")).data
        )

    async def delete(self, message: int | ChatMessage) -> ChatMessage:
        return ChatMessage.model_validate(
            (await self.client.http.delete(f"/messages/{int(message)}")).data
        )
