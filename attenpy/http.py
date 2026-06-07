from typing import Any, Optional, TypedDict, Unpack

import aiohttp

from .exceptions import HTTPException
from .types import AnyResponse, ListResponse, SuccessResponse


class RequestOptions(TypedDict, total=False):
    json: Any
    params: dict[str, Any]


class HTTPClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            headers = {"Authorization": f"Bearer {self.token}"}
            self._session = aiohttp.ClientSession(headers=headers)
        return self._session

    async def request[T](
        self, method: str, path: str, **kwargs: Unpack[RequestOptions]
    ) -> Any:
        if not path.startswith("/"):
            raise ValueError()
        session = await self._get_session()
        url = self.base_url + path

        async with session.request(
            method, url, json=kwargs.get("json"), params=kwargs.get("params")
        ) as resp:
            data: AnyResponse = await resp.json()
            if data["ok"] is False:
                raise HTTPException(resp.status, data)  # TODO statusごとにクラス分ける
        return data

    async def get[T](
        self, typ: type[T], path: str, **kwargs: Unpack[RequestOptions]
    ) -> SuccessResponse[T]:
        return await self.request("GET", path, **kwargs)

    async def get_list[T](
        self, typ: type[T], path: str, **kwargs: Unpack[RequestOptions]
    ) -> ListResponse[T]:
        return await self.request("GET", path, **kwargs)

    async def post[T](
        self, typ: type[T], path: str, **kwargs: Unpack[RequestOptions]
    ) -> SuccessResponse[T]:
        return await self.request("POST", path, **kwargs)

    async def put[T](
        self, typ: type[T], path: str, **kwargs: Unpack[RequestOptions]
    ) -> SuccessResponse[T]:
        return await self.request("PUT", path, **kwargs)

    async def delete[T](
        self, typ: type[T], path: str, **kwargs: Unpack[RequestOptions]
    ) -> SuccessResponse[T]:
        return await self.request("DELETE", path, **kwargs)

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
