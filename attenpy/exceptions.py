from .types import ErrorResponsePayload


class AttenpyException(Exception):
    pass


class HTTPException(AttenpyException):
    def __init__(self, status: int, data: ErrorResponsePayload):
        self.status = status
        self.code = data["code"]
        self.details = data["details"]
        super().__init__(f"HTTP {self.status}: {self.code}")
