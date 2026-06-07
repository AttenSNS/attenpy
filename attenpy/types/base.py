from typing import Literal, TypedDict


class SuccessResponse[T](TypedDict):
    ok: Literal[True]
    data: T


class CursorPage(TypedDict):
    limit: int
    order: Literal["asc", "desc"]
    cursor: int | None
    next: int | None
    back: int | None
    has_more: bool


class ListResponse[T](SuccessResponse[list[T]]):
    page: CursorPage


class ErrorResponse(TypedDict):
    ok: Literal[False]
    code: str
    details: dict


AnyResponse = SuccessResponse | ErrorResponse
