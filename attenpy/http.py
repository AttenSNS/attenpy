import aiohttp
from typing import Optional

from .models import AnyResponse, SuccessResponse
from .exceptions import HTTPException


class HTTPClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            headers = {
                "Authorization": f"Bearer {self.token}"
            }
            self._session = aiohttp.ClientSession(headers=headers)
        return self._session

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> SuccessResponse:
        session = await self._get_session()
        url = f"{self.base_url}{path}"

        async with session.request(
            method, url,
            json=json,
            params=params
        ) as resp:
            data: AnyResponse = await resp.json()
            if data["ok"] is False:
                raise HTTPException(resp.status, data)
            return data

    async def get(self, path: str, **kwargs) -> SuccessResponse:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> SuccessResponse:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs) -> SuccessResponse:
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> SuccessResponse:
        return await self.request("DELETE", path, **kwargs)

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
