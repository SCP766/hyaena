from __future__ import annotations

from uuid import UUID

from sqlalchemy import ColumnElement, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.severity import Severity
from app.enums.issue_status import IssueStatus
from app.issue.model import Issue


class IssueRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def upsert(self, issue: Issue) -> Issue | None:
        stmt = (
            insert(Issue)
            .values(
                id=issue.id,
                fingerprint=issue.fingerprint,
                service=issue.service,
                environment=issue.environment,
                exception_type=issue.exception_type,
                message=issue.message,
                severity=issue.severity,
                status=issue.status,
                first_seen=issue.first_seen,
                last_seen=issue.last_seen,
                occurrence_count=issue.occurrence_count,
            )
            .on_conflict_do_update(
                index_elements=["fingerprint", "service"],
                set_={
                    "last_seen": issue.last_seen,
                    "occurrence_count": Issue.occurrence_count + 1,
                },
            )
            .returning(Issue)
        )
        result = (await self._db.execute(stmt)).scalar_one()
        await self._db.flush()

        self._db.expunge(result)

        return result

    async def get_by_fingerprint(
        self,
        fingerprint: str,
        service: str,
    ) -> Issue | None:
        stmt = (
            select(Issue)
            .where(
                Issue.fingerprint == fingerprint,
                Issue.service == service,
            )
            .limit(1)
        )

        result = (await self._db.execute(stmt)).scalar_one_or_none()

        if result:
            self._db.expunge(result)

        return result

    async def get_by_id(
        self,
        issue_id: UUID,
    ) -> Issue | None:
        stmt = select(Issue).where(Issue.id == issue_id).limit(1)

        result = (await self._db.execute(stmt)).scalar_one_or_none()

        if result:
            self._db.expunge(result)

        return result

    async def list(
        self,
        service: str | None,
        environment: str | None,
        status: IssueStatus | None,
        severity: Severity | None,
        page: int,
        page_size: int,
        order_fields: dict[str, ColumnElement[object]],
    ) -> tuple[int, list[Issue]]:
        offset = (page - 1) * page_size

        conditions: list[ColumnElement[bool]] = []

        if service:
            conditions.append(Issue.service == service)

        if environment:
            conditions.append(Issue.environment == environment)

        if status:
            conditions.append(Issue.status == status)

        if severity:
            conditions.append(Issue.severity == severity)

        stmt = select(Issue).where(*conditions)
        count_stmt = select(func.count()).select_from(stmt.subquery())

        order_by = list(order_fields.values()) or [Issue.last_seen.desc()]
        stmt = stmt.order_by(*order_by).offset(offset).limit(page_size)

        count = await self._db.scalar(count_stmt) or 0
        issues = (await self._db.execute(stmt)).scalars().all()

        self._db.expunge(*issues)

        return count, list(issues)

    async def update_status(
        self,
        issue_id: UUID,
        status: IssueStatus,
    ) -> bool:
        stmt = update(Issue).where(Issue.id == issue_id).values(status=status)

        result = await self._db.execute(stmt)

        return result.rowcount == 1
