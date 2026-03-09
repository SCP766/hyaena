from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.event.model import ErrorEvent
from app.issue.model import Issue
from app.enums.issue_status import IssueStatus
from app.issue.utility.fingerprint_utility import FingerprintUtil


class IssueManager:
    def compute_fingerprint_from_payload(
        self,
        service: str,
        exception_type: str,
        traceback: str,
    ) -> str:
        return FingerprintUtil.compute(
            service=service,
            exception_type=exception_type,
            traceback=traceback,
        )

    def create_from_event(self, event: ErrorEvent) -> Issue:
        return Issue(
            id=uuid4(),
            fingerprint=event.fingerprint,
            service=event.service,
            environment=event.environment,
            exception_type=event.exception_type,
            message=event.message,
            severity=event.severity,
            status=IssueStatus.UNRESOLVED,
            first_seen=event.created_at,
            last_seen=event.created_at,
            occurrence_count=1,
        )

    def increment(self, issue: Issue, occurred_at: datetime) -> Issue:

        issue.last_seen = occurred_at
        issue.occurrence_count += 1
        return issue
