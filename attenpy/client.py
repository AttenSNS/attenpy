from typing import Optional

from .endpoints import UserEndpoint
from .http import HTTPClient


class Client:
    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.atten.win",
    ):
        self.base_url = base_url
        self.http: HTTPClient = HTTPClient(self.base_url, token)
        self._token: Optional[str] = None

        self.users = UserEndpoint(self)

    async def close(self) -> None:
        if self.http:
            await self.http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
