from typing import Any, Literal, TypedDict


class RequestMetaPayload(TypedDict):
    request_id: str
    session_id: str | None
    actor_id: str | None


class SuccessResponsePayload[T](TypedDict):
    ok: Literal[True]
    data: T
    meta: RequestMetaPayload


class CursorPagePayload(TypedDict):
    limit: int
    order: Literal["asc", "desc"]
    cursor: str | None
    next: str | None
    back: str | None
    has_more: bool


class ListResponsePayload[T](SuccessResponsePayload[list[T]]):
    page: CursorPagePayload


class ErrorResponsePayload(TypedDict):
    ok: Literal[False]
    code: str
    details: dict[str, Any]


AnyResponsePayload = SuccessResponsePayload | ErrorResponsePayload
