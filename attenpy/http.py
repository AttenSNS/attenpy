import asyncio
from typing import Any, Optional, TypedDict, Unpack

import aiohttp
from pydantic import ValidationError

from .exceptions import HTTPException, InvalidResponseError
from .models import ErrorResponse, ListResponse, SuccessResponse


class RequestOptions(TypedDict, total=False):
    json: Any
    params: dict[str, Any]


class HTTPClient:
    def __init__(self, base_url: str, token: str | None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._session: Optional[aiohttp.ClientSession] = None
        self._closed: bool = False

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.closed:
            raise RuntimeError("Session is closed")
        if self._session is None or self._session.closed:
            headers = {}
            if self.token:
                headers["Authorization"] = "Bearer " + self.token
            self._session = aiohttp.ClientSession(headers=headers)
        return self._session

    def _parse_response(
        self, payload: Any
    ) -> SuccessResponse[Any] | ListResponse[Any] | ErrorResponse:
        if not isinstance(payload, dict) or "ok" not in payload:
            raise InvalidResponseError(payload)

        try:
            if payload["ok"] is False:
                return ErrorResponse.model_validate(payload)
            if "page" in payload:
                return ListResponse.model_validate(payload)
            return SuccessResponse.model_validate(payload)
        except ValidationError as exc:
            raise InvalidResponseError(payload) from exc

    async def _request(
        self, method: str, path: str, **kw: Unpack[RequestOptions]
    ) -> SuccessResponse[Any] | ListResponse[Any]:
        if not path.startswith("/"):
            raise ValueError("The path must start with /.")
        session = await self._get_session()
        url = self.base_url + path

        while True:
            async with session.request(
                method, url, json=kw.get("json"), params=kw.get("params")
            ) as resp:
                data = self._parse_response(await resp.json())
                if isinstance(data, ErrorResponse):
                    if resp.status == 429 and data.code == "api_latelimit":
                        retry_after = data.details.get("retry_after")
                        if isinstance(retry_after, int | float) and retry_after >= 0:
                            await asyncio.sleep(retry_after)
                            continue
                    raise HTTPException(
                        resp.status, data
                    )  # TODO statusごとにクラス分ける
            return data

    async def get(
        self, path: str, **kw: Unpack[RequestOptions]
    ) -> SuccessResponse[Any]:
        return await self._request("GET", path, **kw)

    async def get_list(
        self, path: str, **kw: Unpack[RequestOptions]
    ) -> ListResponse[Any]:
        data = await self._request("GET", path, **kw)
        if isinstance(data, SuccessResponse):
            raise InvalidResponseError(data.model_dump(mode="python"))
        return data

    async def post(
        self, path: str, **kw: Unpack[RequestOptions]
    ) -> SuccessResponse[Any]:
        return await self._request("POST", path, **kw)

    async def put(
        self, path: str, **kw: Unpack[RequestOptions]
    ) -> SuccessResponse[Any]:
        return await self._request("PUT", path, **kw)

    async def patch(
        self, path: str, **kw: Unpack[RequestOptions]
    ) -> SuccessResponse[Any]:
        return await self._request("PATCH", path, **kw)

    async def delete(
        self, path: str, **kw: Unpack[RequestOptions]
    ) -> SuccessResponse[Any]:
        return await self._request("DELETE", path, **kw)

    @property
    def closed(self):
        return self._closed

    async def close(self) -> None:
        self._closed = True
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
