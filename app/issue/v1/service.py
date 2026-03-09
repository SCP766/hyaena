from __future__ import annotations

import math
from uuid import UUID

from app.core.response.paginated_response import PaginatedResponse
from app.enums.severity import Severity
from app.issue.exception.issue_not_found import IssueNotFoundException
from app.enums.issue_status import IssueStatus
from app.issue.exception.issue_status_update_failed import (
    IssueStatusUpdateFailedException,
)
from app.issue.repository import IssueRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.issue.v1.responses.issue_reponse import IssueResponse


class IssueService:
    def __init__(
        self, issue_repository: IssueRepository, session: AsyncSession
    ) -> None:
        self.session = session
        self._issue_repository = issue_repository

    async def list_issues(
        self,
        service: str | None,
        environment: str | None,
        status: IssueStatus | None,
        severity: Severity | None,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[list[IssueResponse]]:
        count, issues = await self._issue_repository.list(
            service=service,
            environment=environment,
            status=status,
            severity=severity,
            page=page,
            page_size=page_size,
            order_fields={},
        )

        return PaginatedResponse(
            total=count,
            page=page,
            pages=math.ceil(count / page_size),
            items=[IssueResponse.from_entity(issue) for issue in issues],
        )

    async def get_issue(
        self,
        issue_id: UUID,
    ) -> IssueResponse:
        issue = await self._issue_repository.get_by_id(issue_id)
        if issue is None:
            raise IssueNotFoundException(str(issue_id))
        return IssueResponse.from_entity(issue)

    async def update_status(
        self,
        issue_id: UUID,
        status: IssueStatus,
    ) -> None:
        issue = await self._issue_repository.get_by_id(issue_id)
        if issue is None:
            raise IssueNotFoundException(str(issue_id))
        result = await self._issue_repository.update_status(issue_id, status)

        if not result:
            raise IssueStatusUpdateFailedException(issue_uuid=str(issue_id))

        await self.session.commit()
