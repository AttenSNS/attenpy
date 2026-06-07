from typing import Literal, TypedDict


class SuccessResponsePayload[T](TypedDict):
    ok: Literal[True]
    data: T


class CursorPagePayload(TypedDict):
    limit: int
    order: Literal["asc", "desc"]
    cursor: int | None
    next: int | None
    back: int | None
    has_more: bool


class ListResponsePayload[T](SuccessResponsePayload[list[T]]):
    page: CursorPagePayload


class ErrorResponsePayload(TypedDict):
    ok: Literal[False]
    code: str
    details: dict


AnyResponsePayload = SuccessResponsePayload | ErrorResponsePayload
