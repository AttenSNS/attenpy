from typing import Any, Optional, TypedDict, Unpack, cast

import aiohttp

from .exceptions import HTTPException
from .models import ListResponse, SuccessResponse
from .types import AnyResponsePayload


class RequestOptions(TypedDict, total=False):
    json: Any
    params: dict[str, Any]


class HTTPClient:
    def __init__(self, base_url: str, token: str | None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            headers = {}
            if self.token:
                headers["Authorization"] = "Bearer " + self.token
            self._session = aiohttp.ClientSession(headers=headers)
        return self._session

    async def _request[T](
        self, method: str, path: str, **kw: Unpack[RequestOptions]
    ) -> Any:
        if not path.startswith("/"):
            raise ValueError()
        session = await self._get_session()
        url = self.base_url + path

        async with session.request(
            method, url, json=kw.get("json"), params=kw.get("params")
        ) as resp:
            data = cast(AnyResponsePayload, await resp.json())  # TODO レスポンスの検証
            if data["ok"] is False:
                raise HTTPException(resp.status, data)  # TODO statusごとにクラス分ける
                # TODO 429
        return data

    async def get(self, path: str, **kw: Unpack[RequestOptions]) -> SuccessResponse:
        data = await self._request("GET", path, **kw)
        return SuccessResponse.from_json(data)

    async def get_list(self, path: str, **kw: Unpack[RequestOptions]) -> ListResponse:
        data = await self._request("GET", path, **kw)
        return ListResponse.from_json(data)

    async def post(self, path: str, **kw: Unpack[RequestOptions]) -> SuccessResponse:
        data = await self._request("POST", path, **kw)
        return SuccessResponse.from_json(data)

    async def put(self, path: str, **kw: Unpack[RequestOptions]) -> SuccessResponse:
        data = await self._request("PUT", path, **kw)
        return SuccessResponse.from_json(data)

    async def patch(self, path: str, **kw: Unpack[RequestOptions]) -> SuccessResponse:
        data = await self._request("PATCH", path, **kw)
        return SuccessResponse.from_json(data)

    async def delete(self, path: str, **kw: Unpack[RequestOptions]) -> SuccessResponse:
        data = await self._request("DELETE", path, **kw)
        return SuccessResponse.from_json(data)

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
