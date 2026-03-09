from fastapi import status

from app.core.exception.base import BaseCustomException


class InvalidAPIKeyException(BaseCustomException):
    def __init__(
        self,
        detail: str = "Invalid API Key",
        status_code: int = status.HTTP_403_FORBIDDEN,
    ) -> None:
        super().__init__(detail, status_code)
