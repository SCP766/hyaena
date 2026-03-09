from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.event.model import ErrorEvent
from app.enums.severity import Severity


class ErrorEventResponse(BaseModel):
    id: UUID
    fingerprint: str
    service: str
    environment: str
    exception_type: str
    message: str
    traceback: str
    severity: Severity
    release: str | None
    user_id: str | None
    request_path: str | None
    request_method: str | None
    extra: dict[str, str]
    created_at: datetime

    @classmethod
    def from_entity(cls, event: ErrorEvent) -> ErrorEventResponse:
        return cls(
            id=event.id,
            fingerprint=event.fingerprint,
            service=event.service,
            environment=event.environment,
            exception_type=event.exception_type,
            message=event.message,
            traceback=event.traceback,
            severity=Severity(event.severity),
            release=event.release,
            user_id=event.user_id,
            request_path=event.request_path,
            request_method=event.request_method,
            extra=event.extra,
            created_at=event.created_at,
        )
