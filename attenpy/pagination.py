from collections.abc import AsyncIterator
from typing import Any, Literal, TypeVar

from .http import HTTPClient

ItemT = TypeVar("ItemT")
CursorT = TypeVar("CursorT")

MAX_PAGINATION_LIMIT = 30

PAGINATE_ORDER = Literal["desc", "asc"]
PAGINATE_ORDER_DEFAULT: PAGINATE_ORDER = "desc"


async def paginate(
    http: HTTPClient,
    path: str,
    *,
    cursor: int | None,
    limit: int,
    order: PAGINATE_ORDER,
    params: dict[str, Any] | None = None,
) -> AsyncIterator:
    params = (params and params.copy()) or {}
    params["order"] = order
    if cursor is not None:
        params["cursor"] = cursor
    remaining = limit
    while remaining > 0:
        params["limit"] = min(remaining, MAX_PAGINATION_LIMIT)
        resp = await http.get_list(path, params=params)
        for item in resp.data:
            yield item
            remaining -= 1
            if remaining == 0:
                return
        if not resp.page.has_more:
            break
        params["cursor"] = resp.page.next
