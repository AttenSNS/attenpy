from collections.abc import AsyncIterator
from typing import Any, Literal, TypeVar

from .http import HTTPClient

ItemT = TypeVar("ItemT")
CursorT = TypeVar("CursorT")

MAX_PAGINATION_LIMIT = 30

PAGINATE_ORDER = Literal["desc", "asc"]


async def paginate[ItemT](
    typ: type[ItemT],
    http: HTTPClient,
    path: str,
    cursor: int | None = None,
    *,
    limit: int = MAX_PAGINATION_LIMIT,
    params: dict[str, Any] | None = None,
    order: PAGINATE_ORDER,
) -> AsyncIterator[ItemT]:
    params = (params and params.copy()) or {}
    params["order"] = order
    if cursor is not None:
        params["cursor"] = cursor
    remaining = limit
    while remaining > 0:
        params["limit"] = min(remaining, MAX_PAGINATION_LIMIT)
        resp = await http.get_list(typ, path, params=params)
        for item in resp["data"]:
            yield item
            remaining -= 1
            if remaining == 0:
                return
        page = resp["page"]
        if not page["has_more"]:
            break
        params["cursor"] = page["next"]
