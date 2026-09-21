from typing import Any


def int_or_none(obj: Any) -> int | None:
    return None if obj is None else int(obj)


def api_bool(val: bool) -> str:
    return "1" if val else "0"
