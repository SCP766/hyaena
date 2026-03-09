from __future__ import annotations

from enum import StrEnum


class IssueStatus(StrEnum):
    UNRESOLVED = "unresolved"
    RESOLVED = "resolved"
    IGNORED = "ignored"
