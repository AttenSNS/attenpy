from typing import Any

from .models import ErrorResponse


class AttenpyException(Exception):
    pass


class InvalidResponseError(AttenpyException):
    def __init__(self, payload: Any):
        self.payload = payload
        super().__init__("invalid response payload")


class HTTPException(AttenpyException):
    def __init__(self, status: int, data: ErrorResponse):
        self.status = status
        self.code = data.code
        self.details = data.details
        super().__init__(f"HTTP {self.status}: {self.code}")
