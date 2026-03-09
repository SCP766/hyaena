from app.core.session import get_db_session
from app.event.repository import ErrorEventRepository
from app.event.v1.service import EventService
from app.issue.repository import IssueRepository


async def get_event_service() -> EventService:
    async with get_db_session() as session:
        event_repository = ErrorEventRepository(session=session)
        issue_repository = IssueRepository(session=session)

        return EventService(
            event_repository=event_repository,
            issue_repository=issue_repository,
            session=session,
        )
