from __future__ import annotations

from uuid import UUID
from fastapi import status
from fastapi import APIRouter, Depends

from app.core.response.paginated_response import PaginatedResponse
from app.enums.issue_status import IssueStatus
from app.enums.severity import Severity
from app.issue.dependency import get_issue_service
from app.middleware.api_key.api_key import verify_x_api_key
from app.issue.v1.responses.issue_reponse import IssueResponse
from app.issue.v1.schemas.schema import UpdateIssueStatusSchema
from app.issue.v1.service import IssueService

router = APIRouter(prefix="/v1/issues", dependencies=[Depends(verify_x_api_key)])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[list[IssueResponse]],
)
async def list_issues(
    svc: str | None = None,
    environment: str | None = None,
    issue_status: IssueStatus | None = None,
    severity: Severity | None = None,
    page: int = 0,
    page_size: int = 50,
    service: IssueService = Depends(get_issue_service),
) -> PaginatedResponse[list[IssueResponse]]:
    return await service.list_issues(
        service=svc,
        environment=environment,
        status=issue_status,
        severity=severity,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{issue_id}",
    status_code=status.HTTP_200_OK,
    response_model=IssueResponse,
)
async def get_issue(
    issue_id: UUID,
    service: IssueService = Depends(get_issue_service),
) -> IssueResponse:
    return await service.get_issue(issue_id)


@router.patch(
    "/{issue_id}/status",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_issue_status(
    issue_id: UUID,
    body: UpdateIssueStatusSchema,
    service: IssueService = Depends(get_issue_service),
):
    await service.update_status(issue_id, IssueStatus(body.status))
