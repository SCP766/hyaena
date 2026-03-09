from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.severity import Severity


class IngestEventSchema(BaseModel):
    event_id: UUID
    service: str = Field(min_length=1, max_length=128)
    environment: str = Field(min_length=1, max_length=64)
    release: str | None = Field(default=None, max_length=128)
    exception_type: str = Field(min_length=1, max_length=256)
    message: str = Field(min_length=1)
    traceback: str
    severity: Severity = Severity.ERROR
    timestamp: datetime
    tags: dict[str, str] = Field(default_factory=dict)
    user: dict[str, str] = Field(default_factory=dict)
    extra: dict[str, str] = Field(default_factory=dict)
