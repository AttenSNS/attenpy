from collections.abc import AsyncIterator, Sequence
from typing import TYPE_CHECKING, Unpack

from ..models import Notice
from ..models.notice import NoticeType
from ..pagination import PaginateOptions, paginate
from ..payloads import NoticeUnreadCountPayload

if TYPE_CHECKING:
    from ..client import Client


class NoticeEndpoint:
    def __init__(self, client: "Client"):
        self.client = client

    async def list(
        self,
        *,
        types: Sequence[NoticeType] | None = None,
        **kw: Unpack[PaginateOptions],
    ) -> AsyncIterator[Notice]:
        params = None
        if types:
            params = {"type": list(dict.fromkeys(types))}
        async for data in paginate(self.client.http, "/notices", params=params, **kw):
            yield Notice.model_validate(data)

    async def read_up_to(self, notice: int | Notice):
        await self.client.http.put(
            "/notices/read-up-to", json={"notice_id": int(notice)}
        )

    async def get_unread_count(self) -> NoticeUnreadCountPayload:
        return NoticeUnreadCountPayload.model_validate(
            (await self.client.http.get("/notices/unread-count")).data
        )
