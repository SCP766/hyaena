from fastapi import APIRouter

from app.core.docs.route import router as docs_router
from app.core.health.route import router as health_router
from app.event.v1.route import router as event_router
from app.issue.v1.route import router as issue_router


routers: list[APIRouter] = [
    docs_router,
    health_router,
    event_router,
    issue_router,
]
