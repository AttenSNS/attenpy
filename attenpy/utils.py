def int_or_none(obj: str | None) -> int | None:
    return None if obj is None else int(obj)
