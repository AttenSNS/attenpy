from collections.abc import AsyncIterator
from typing import Any, Literal, TypedDict, TypeVar, Unpack

from .http import HTTPClient

ItemT = TypeVar("ItemT")
CursorT = TypeVar("CursorT")

MAX_PAGINATION_LIMIT = 30

PAGINATE_ORDER = Literal["desc", "asc"]
PAGINATE_ORDER_DEFAULT: PAGINATE_ORDER = "desc"


class PaginateOptions(TypedDict, total=False):
    cursor: int
    limit: int
    order: PAGINATE_ORDER


async def paginate(
    http: HTTPClient,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    **kw: Unpack[PaginateOptions],
) -> AsyncIterator:
    params = (params and params.copy()) or {}
    params["order"] = kw.get("order", PAGINATE_ORDER_DEFAULT)
    if "cursor" in kw:
        params["cursor"] = kw["cursor"]
    remaining = kw.get("limit", MAX_PAGINATION_LIMIT)
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
