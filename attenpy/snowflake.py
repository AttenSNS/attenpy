from __future__ import annotations

from datetime import UTC, datetime
from typing import Final, Self

EPOCH_DATETIME = datetime(2026, 1, 1, 0, 0, 0, 0, tzinfo=UTC)
EPOCH_MS = int(EPOCH_DATETIME.timestamp() * 1000)

WORKER_ID_BITS = 8
SEQUENCE_BITS = 12

MAX_SNOWFLAKE = 2**63 - 1
MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

WORKER_ID_SHIFT = SEQUENCE_BITS
TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS


class Snowflake:
    def __init__(self, value: int) -> None:
        self.value: Final[int] = value

    @classmethod
    def parse(cls, value: int | str | "Snowflake") -> Self:
        if isinstance(value, Snowflake):
            return cls(value.value)

        if isinstance(value, int):
            if 0 <= value <= MAX_SNOWFLAKE:
                return cls(value)
            raise ValueError(f"snowflake must be between 0 and {MAX_SNOWFLAKE}")

        if isinstance(value, str):
            text = value.strip()
            if not text.isdecimal():
                raise ValueError("snowflake must be a decimal string")
            parsed = int(text)
            if 0 <= parsed <= MAX_SNOWFLAKE:
                return cls(parsed)
            raise ValueError(f"snowflake must be between 0 and {MAX_SNOWFLAKE}")

        raise TypeError("snowflake must be an integer or decimal string")

    @classmethod
    def from_datetime(cls, dt: datetime, *, is_max: bool = False) -> Self:
        ts_ms = int(dt.timestamp() * 1000)
        offset_ms = ts_ms - EPOCH_MS

        if is_max:
            return cls(
                (offset_ms << TIMESTAMP_SHIFT)
                | (MAX_WORKER_ID << WORKER_ID_SHIFT)
                | MAX_SEQUENCE
            )
        return cls(offset_ms << TIMESTAMP_SHIFT)

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)

    @property
    def timestamp_ms(self) -> int:
        return (self.value >> TIMESTAMP_SHIFT) + EPOCH_MS

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp_ms / 1000, tz=UTC)

    @property
    def created_at(self) -> datetime:
        return self.datetime

    @property
    def worker_id(self) -> int:
        return (self.value >> WORKER_ID_SHIFT) & MAX_WORKER_ID

    @property
    def sequence(self) -> int:
        return self.value & MAX_SEQUENCE

    @property
    def offset_ms(self) -> int:
        return self.timestamp_ms - EPOCH_MS
