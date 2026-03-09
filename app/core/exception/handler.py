from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exception.base import BaseCustomException


async def global_exception_handler(request: Request, exc: BaseCustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "detail": exc.detail,
        },
    )
