from .types import ErrorResponse


class AttenpyException(Exception):
    pass


class APIConnectionError(AttenpyException):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class HTTPException(AttenpyException):
    def __init__(self, status: int, data: ErrorResponse):
        self.status = status
        self.code = data["code"]
        self.details = data["details"]
        super().__init__(f"HTTP {self.status}: {self.code}")
