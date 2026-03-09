from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.event.model import ErrorEvent


class ErrorEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def save_batch(
        self,
        events: list[ErrorEvent],
    ) -> None:
        self._db.add_all(
            [
                ErrorEvent(
                    id=e.id,
                    fingerprint=e.fingerprint,
                    service=e.service,
                    environment=e.environment,
                    exception_type=e.exception_type,
                    message=e.message,
                    traceback=e.traceback,
                    severity=e.severity,
                    release=e.release,
                    user_id=e.user_id,
                    request_path=e.request_path,
                    request_method=e.request_method,
                    extra=e.extra,
                    created_at=e.created_at,
                )
                for e in events
            ]
        )
        await self._db.commit()

    async def get_by_id(
        self,
        event_id: UUID,
    ) -> ErrorEvent | None:
        stmt = select(ErrorEvent).where(ErrorEvent.id == event_id).limit(1)

        result = (await self._db.execute(stmt)).scalar_one_or_none()

        if result:
            self._db.expunge(result)

        return result

    async def list_by_issue(
        self,
        fingerprint: str,
        service: str,
        page: int,
        page_size: int,
    ) -> tuple[int, list[ErrorEvent]]:
        offset = (page - 1) * page_size

        stmt = select(ErrorEvent).where(
            ErrorEvent.fingerprint == fingerprint,
            ErrorEvent.service == service,
        )
        count_stmt = select(func.count()).select_from(stmt.subquery())

        stmt = stmt.offset(offset).limit(page_size)

        count = await self._db.scalar(count_stmt) or 0
        events = (await self._db.execute(stmt)).scalars().all()

        self._db.expunge(*events)

        return count, list(events)
