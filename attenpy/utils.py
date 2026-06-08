from typing import Any


def int_or_none(obj: Any) -> int | None:
    return None if obj is None else int(obj)
