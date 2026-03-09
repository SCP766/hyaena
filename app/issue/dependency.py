from app.core.session import get_db_session
from app.issue.v1.service import IssueService
from app.issue.repository import IssueRepository


async def get_issue_service() -> IssueService:
    async with get_db_session() as session:
        issue_repository = IssueRepository(session=session)

        return IssueService(
            issue_repository=issue_repository,
            session=session,
        )
