from __future__ import annotations

from pydantic import BaseModel, Field


class UpdateIssueStatusSchema(BaseModel):
    status: str = Field(min_length=1)
