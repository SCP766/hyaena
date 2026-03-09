from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.core.response.paginated_response import PaginatedResponse
from app.event.dependency import get_event_service
from app.event.v1.responses.error_event_response import ErrorEventResponse
from app.event.v1.schemas.schema import IngestEventSchema
from app.event.v1.service import EventService
from app.middleware.api_key.api_key import verify_x_api_key

router = APIRouter(prefix="/v1/events", dependencies=[Depends(verify_x_api_key)])


@router.post(
    path="/",
    status_code=status.HTTP_202_ACCEPTED,
)
async def ingest_event(
    payload: IngestEventSchema,
    service: EventService = Depends(get_event_service),
) -> None:
    await service.ingest_batch([payload])


@router.get(
    path="by-issue/{issue_id}",
    response_model=PaginatedResponse[list[ErrorEventResponse]],
)
async def list_events_by_issue(
    issue_id: UUID,
    page: int = Query(ge=1),
    page_size: int = Query(ge=20, le=100),
    service: EventService = Depends(get_event_service),
) -> PaginatedResponse[list[ErrorEventResponse]]:
    return await service.list_by_issue(issue_id, page=page, page_size=page_size)
