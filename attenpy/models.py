

from typing import Any, Literal, TypedDict


class SuccessResponse(TypedDict):
    ok: Literal[True]
    data: Any


class CursorPage(TypedDict):
    limit: int
    order: Literal["asc", "desc"]
    cursor: int | None
    next: int | None
    back: int | None
    has_more: bool


class ListResponse(SuccessResponse):
    page: CursorPage


class ErrorResponse(TypedDict):
    ok: Literal[False]
    code: str
    details: dict


AnyResponse = SuccessResponse | ErrorResponse
