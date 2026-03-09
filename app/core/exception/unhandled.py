from fastapi import status

from app.core.exception.base import BaseCustomException


class UnhandledException(BaseCustomException):
    def __init__(
        self,
        detail: str = "Unhandled Exception",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:

        super().__init__(detail, status_code)
