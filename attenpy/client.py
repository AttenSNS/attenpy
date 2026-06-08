import asyncio
from typing import Optional

from .endpoints import UserEndpoint
from .http import HTTPClient


class Client:
    def __init__(
        self,
        base_url: str = "https://api.atten.win",
    ):
        self.base_url = base_url
        self.http: Optional[HTTPClient] = None
        self._token: Optional[str] = None
        self._ready: asyncio.Event = asyncio.Event()

        self.users = UserEndpoint(self)

    async def login(self, token: str) -> None:
        self._token = token
        self.http = HTTPClient(self.base_url, token)
        self._ready.set()

    async def start(self, token: str) -> None:
        await self.login(token)

    async def close(self) -> None:
        if self.http:
            await self.http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
