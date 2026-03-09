from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.engine import engine

router = APIRouter(tags=["Health"])


@router.get("/health", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@router.get("/health/ready", include_in_schema=False)
async def ready() -> JSONResponse:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return JSONResponse(content={"status": "ok", "db": "ok"})
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={"status": "unavailable", "db": str(exc)},
        )
