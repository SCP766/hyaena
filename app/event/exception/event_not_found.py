from __future__ import annotations
from fastapi import status
from app.core.exception.base import BaseCustomException


class EventNotFoundException(BaseCustomException):
    def __init__(self, event_id: str) -> None:
        super().__init__(
            detail=f"Event '{event_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
