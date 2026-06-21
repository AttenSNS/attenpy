from __future__ import annotations

import asyncio
from collections.abc import Callable
from contextlib import suppress
from json import JSONDecodeError
from typing import TYPE_CHECKING, Any, Coroutine
from urllib.parse import urlencode, urlsplit, urlunsplit

import aiohttp
from pydantic import BaseModel

from .models import Notice
from .payloads import (
    BotReadyPayload,
    WsTokenPayload,
)
from .ref import UserRef

if TYPE_CHECKING:
    from .client import Client

EventHandler = Callable[[Any], Coroutine[Any, Any, Any]]

EVENT_PAYLOAD_MODELS: dict[str, type[BaseModel]] = {
    "bot.ready": BotReadyPayload,
    "notice.created": Notice,
}


class WSClient:
    def __init__(self, client: "Client"):
        self.client = client
        self._handlers: dict[str, EventHandler] = {}
        self._task: asyncio.Task[None] | None = None
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._closing = False

    @property
    def event_payload_models(self) -> dict[str, type[BaseModel]]:
        return EVENT_PAYLOAD_MODELS.copy()

    def add_handler(self, event_name: str, func: EventHandler) -> None:
        self._require_event_name(event_name)
        if event_name in self._handlers:
            raise ValueError(f"handler already registered for {event_name}")
        self._handlers[event_name] = func

    def remove_handler(self, event_name: str) -> None:
        self._require_event_name(event_name)
        if event_name not in self._handlers:
            raise ValueError(f"handler not registered for {event_name}")
        self._handlers.pop(event_name)

    async def connect(self, *, reconnect: bool = False) -> None:
        self._assert_not_running()
        self._closing = False
        self._task = asyncio.create_task(self._run_background(reconnect=reconnect))
        self._task.add_done_callback(self._consume_task_exception)

    async def start(self, *, reconnect: bool = False) -> None:
        self._assert_not_running()
        self._closing = False
        await self._run(reconnect=reconnect)

    async def disconnect(self) -> None:
        self._closing = True

        ws = self._ws
        if ws is not None and not ws.closed:
            await ws.close()

        task = self._task
        if task is None:
            return

        if task.done():
            with suppress(asyncio.CancelledError):
                await task
            self._task = None
            return

        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
        self._task = None

    async def _run_background(self, *, reconnect: bool) -> None:
        try:
            await self._run(reconnect=reconnect)
        finally:
            current = asyncio.current_task()
            if current is not None and self._task is current:
                self._task = None

    async def _run(self, *, reconnect: bool) -> None:
        while not self._closing:
            try:
                await self._run_once()
                return
            except asyncio.CancelledError:
                raise
            except Exception:
                if not reconnect or self._closing:
                    raise
                await asyncio.sleep(1)

    async def _run_once(self) -> None:
        token = await self._fetch_ws_token()
        session = await self.client.http._get_session()

        async with session.ws_connect(self._build_ws_url(token)) as ws:
            self._ws = ws
            try:
                async for message in ws:
                    if message.type != aiohttp.WSMsgType.TEXT:
                        if message.type in {
                            aiohttp.WSMsgType.CLOSE,
                            aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.CLOSING,
                            aiohttp.WSMsgType.ERROR,
                        }:
                            break
                        continue

                    try:
                        payload = message.json()
                    except (TypeError, JSONDecodeError):
                        continue

                    if not isinstance(payload, dict):
                        continue

                    event_name = payload.get("type")
                    data = payload.get("data")
                    if not isinstance(event_name, str) or not isinstance(data, dict):
                        continue

                    await self._dispatch(event_name, data)
            finally:
                self._ws = None

    async def _fetch_ws_token(self) -> str:
        response = await self.client.http.post(f"/users/{UserRef.ME}/bot/ws-token")
        payload = WsTokenPayload.model_validate(response.data)
        return payload.token

    def _build_ws_url(self, token: str) -> str:
        parsed = urlsplit(self.client.base_url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        query = urlencode({"token": token})
        return urlunsplit((scheme, parsed.netloc, "/ws", query, ""))

    async def _dispatch(self, event_name: str, data: dict[str, Any]) -> None:
        model = EVENT_PAYLOAD_MODELS.get(event_name)
        if model is None:
            return

        validated = model.model_validate(data)
        handler = self._handlers.get(event_name)
        if handler is None:
            return

        asyncio.create_task(handler(validated))

    def _require_event_name(self, event_name: str) -> None:
        if event_name not in EVENT_PAYLOAD_MODELS:
            raise ValueError(f"unknown event_name: {event_name}")

    def _assert_not_running(self) -> None:
        if self._task is not None and not self._task.done():
            raise RuntimeError("websocket listener is already running")

        ws = self._ws
        if ws is not None and not ws.closed:
            raise RuntimeError("websocket listener is already running")

    @staticmethod
    def _consume_task_exception(task: asyncio.Task[None]) -> None:
        with suppress(asyncio.CancelledError):
            task.exception()
