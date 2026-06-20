from .endpoints import NoticeEndpoint, PostEndpoint, UserEndpoint
from .http import HTTPClient
from .ref import UserRef
from .ws import WSClient


class Client:
    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.atten.win",
    ):
        self.base_url = base_url
        self.http: HTTPClient = HTTPClient(self.base_url, token)
        self.ws = WSClient(self)

        self.users = UserEndpoint(self)
        self.posts = PostEndpoint(self)
        self.notices = NoticeEndpoint(self)

    def add_handler(self, event_name: str, func):
        self.ws.add_handler(event_name, func)

    def remove_handler(self, event_name: str):
        self.ws.remove_handler(event_name)

    def on(self, event_name: str):
        return self.ws.on(event_name)

    async def connect_ws(self, user: UserRef | str, reconnect: bool = False) -> None:
        await self.ws.connect(user, reconnect=reconnect)

    async def start_ws(self, user: UserRef | str, reconnect: bool = False) -> None:
        await self.ws.start(user, reconnect=reconnect)

    async def disconnect_ws(self) -> None:
        await self.ws.disconnect()

    async def close(self) -> None:
        await self.disconnect_ws()
        if self.http:
            await self.http.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
