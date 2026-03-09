from fastapi import status
from app.core.exception.base import BaseCustomException


class IssueStatusUpdateFailedException(BaseCustomException):
    def __init__(
        self,
        issue_uuid: str,
    ) -> None:
        super().__init__(
            detail=f"Failed to update issue '{issue_uuid}'.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
