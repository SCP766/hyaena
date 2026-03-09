from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.enums.severity import Severity
from app.issue.model import Issue
from app.enums.issue_status import IssueStatus


class IssueResponse(BaseModel):
    id: UUID
    fingerprint: str
    service: str
    environment: str
    exception_type: str
    message: str
    severity: Severity
    status: IssueStatus
    first_seen: datetime
    last_seen: datetime
    occurrence_count: int

    @classmethod
    def from_entity(cls, issue: Issue) -> "IssueResponse":
        return cls(
            id=issue.id,
            fingerprint=issue.fingerprint,
            service=issue.service,
            environment=issue.environment,
            exception_type=issue.exception_type,
            message=issue.message,
            severity=Severity(issue.severity),
            status=IssueStatus(issue.status),
            first_seen=issue.first_seen,
            last_seen=issue.last_seen,
            occurrence_count=issue.occurrence_count,
        )
