from dataclasses import dataclass
from typing import Generic, Self, TypeVar

from ..types import (
    CursorPagePayload,
    ListResponsePayload,
    RequestMetaPayload,
    SuccessResponsePayload,
)
from ..utils import int_or_none

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class RequestMeta:
    request_id: str
    session_id: int | None
    actor_id: int | None

    @classmethod
    def from_json(cls, data: RequestMetaPayload) -> Self:
        return cls(
            data["request_id"],
            int_or_none(data["session_id"]),
            int_or_none(data["actor_id"]),
        )


@dataclass(frozen=True, slots=True)
class SuccessResponse(Generic[T]):
    ok: bool
    meta: RequestMeta
    data: T

    @classmethod
    def from_json(cls, data: SuccessResponsePayload) -> Self:
        return cls(
            data["ok"],
            RequestMeta.from_json(data["meta"]),
            data["data"],
        )


@dataclass(frozen=True, slots=True)
class CursorPage:
    limit: int
    order: str
    cursor: int | None
    next: int | None
    back: int | None
    has_more: bool

    @classmethod
    def from_json(cls, data: CursorPagePayload) -> Self:
        return cls(
            data["limit"],
            data["order"],
            int_or_none(data["cursor"]),
            int_or_none(data["next"]),
            int_or_none(data["back"]),
            data["has_more"],
        )


@dataclass(frozen=True, slots=True)
class ListResponse(Generic[T]):
    ok: bool
    meta: RequestMeta
    data: list[T]
    page: CursorPage

    @classmethod
    def from_json(cls, data: ListResponsePayload) -> Self:
        return cls(
            data["ok"],
            RequestMeta.from_json(data["meta"]),
            data["data"],
            CursorPage.from_json(data["page"]),
        )
