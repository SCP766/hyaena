from __future__ import annotations

import logging
import math
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.response.paginated_response import PaginatedResponse
from app.event.model import ErrorEvent
from app.event.repository import ErrorEventRepository
from app.event.v1.responses.error_event_response import ErrorEventResponse
from app.event.v1.schemas.schema import IngestEventSchema
from app.issue.exception.issue_not_found import IssueNotFoundException
from app.issue.manager import IssueManager
from app.issue.utility.fingerprint_utility import FingerprintUtil
from app.issue.repository import IssueRepository


logger = logging.getLogger(__name__)

_issue_manager = IssueManager()
_fingerprint_util = FingerprintUtil()


class EventService:
    def __init__(
        self,
        session: AsyncSession,
        event_repository: ErrorEventRepository,
        issue_repository: IssueRepository,
    ) -> None:
        self._db = session
        self._event_repository = event_repository
        self._issue_repository = issue_repository

    async def ingest_batch(self, payloads: list[IngestEventSchema]) -> None:
        events: list[ErrorEvent] = []

        for payload in payloads:
            fingerprint = _fingerprint_util.compute(
                service=payload.service,
                exception_type=payload.exception_type,
                traceback=payload.traceback,
            )

            event = ErrorEvent(
                id=payload.event_id,
                fingerprint=fingerprint,
                service=payload.service,
                environment=payload.environment,
                exception_type=payload.exception_type,
                message=payload.message,
                traceback=payload.traceback,
                severity=payload.severity,
                release=payload.release,
                user_id=payload.user.get("id"),
                request_path=payload.tags.get("endpoint"),
                request_method=payload.tags.get("method"),
                extra=payload.extra,
                created_at=payload.timestamp,
            )
            events.append(event)

            existing = await self._issue_repository.get_by_fingerprint(
                fingerprint=fingerprint,
                service=payload.service,
            )

            if existing is None:
                issue = _issue_manager.create_from_event(event)
            else:
                issue = _issue_manager.increment(existing, event.created_at)

            await self._issue_repository.upsert(issue)

        await self._event_repository.save_batch(events)

    async def list_by_issue(
        self,
        issue_id: UUID,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[list[ErrorEventResponse]]:
        issue = await self._issue_repository.get_by_id(issue_id)
        if issue is None:
            raise IssueNotFoundException(str(issue_id))

        count, events = await self._event_repository.list_by_issue(
            fingerprint=issue.fingerprint,
            service=issue.service,
            page=page,
            page_size=page_size,
        )

        return PaginatedResponse(
            total=count,
            page=page,
            pages=math.ceil(count / page_size),
            items=[ErrorEventResponse.from_entity(event) for event in events],
        )
