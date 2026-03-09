from __future__ import annotations


class BaseCustomException(Exception):
    def __init__(
        self,
        detail: str = "Internal Server Error",
        status_code: int = 500,
    ) -> None:
        """
        Initializes the BaseCustomException.

        Args:
            detail (str): Error message. Defaults to "Internal Server Error".
            status_code (int): HTTP status code. Defaults to 500.
        """
        self.detail = detail
        self.status_code = status_code
