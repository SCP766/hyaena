from __future__ import annotations
from fastapi import status
from app.core.exception.base import BaseCustomException


class IssueNotFoundException(BaseCustomException):
    def __init__(self, issue_id: str) -> None:
        super().__init__(
            detail=f"Issue '{issue_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
