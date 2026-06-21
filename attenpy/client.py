import asyncio

from .endpoints import NoticeEndpoint, PostEndpoint, UserEndpoint
from .http import HTTPClient
from .ws import EventHandler, WSClient


class _EventHandlerRegister:
    def __init__(self, wsclient: "WSClient", event_name: str):
        self.wsclient = wsclient
        self.wsclient._require_event_name(event_name)
        self.event_name = event_name

    def __call__[T: EventHandler](self, func: T) -> T:
        self.wsclient.add_handler(self.event_name, func)
        return func


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

        self._closed_event = asyncio.Event()

    # websocket

    def add_handler(self, event_name: str, func):
        self.ws.add_handler(event_name, func)

    def remove_handler(self, event_name: str):
        self.ws.remove_handler(event_name)

    def on(self, event_name: str):
        return _EventHandlerRegister(self.ws, event_name)

    async def connect_ws(self, *, reconnect: bool = False) -> None:
        await self.ws.connect(reconnect=reconnect)

    async def start_ws(self, *, reconnect: bool = False) -> None:
        await self.ws.start(reconnect=reconnect)

    async def disconnect_ws(self) -> None:
        await self.ws.disconnect()

    # management

    async def start(self, connect_ws: bool = True):
        async with self:
            if connect_ws:
                await self.start_ws(reconnect=True)
            await self.wait_until_closed()

    def run(self, connect_ws: bool = True):
        asyncio.run(self.start(connect_ws))

    async def wait_until_closed(self):
        return await self._closed_event.wait()

    async def close(self) -> None:
        await self.disconnect_ws()
        await self.http.close()
        self._closed_event.set()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
