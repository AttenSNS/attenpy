from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, field_validator

from ..utils import int_or_none

T = TypeVar("T")


def _normalize_optional_snowflake(value: Any) -> int | None:
    return int_or_none(value)


class RequestMeta(BaseModel):
    request_id: str
    session_id: int | None
    actor_id: int | None

    @field_validator("session_id", "actor_id", mode="before")
    @classmethod
    def validate_ids(cls, value: Any) -> int | None:
        return _normalize_optional_snowflake(value)


class SuccessResponse(BaseModel, Generic[T]):
    ok: Literal[True]
    meta: RequestMeta
    data: T


class CursorPage(BaseModel):
    limit: int
    order: str
    cursor: int | None
    next: int | None
    back: int | None
    has_more: bool

    @field_validator("cursor", "next", "back", mode="before")
    @classmethod
    def validate_cursors(cls, value: Any) -> int | None:
        return _normalize_optional_snowflake(value)


class ListResponse(SuccessResponse[list[T]], Generic[T]):
    page: CursorPage


class ErrorResponse(BaseModel):
    ok: Literal[False]
    code: str
    details: dict[str, Any]
