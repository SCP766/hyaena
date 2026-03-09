from __future__ import annotations


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exception.base import BaseCustomException
from app.core.lifespan import lifespan
from app.core.routes import routers


app = FastAPI(title="Hyaena", version="0.1.0", lifespan=lifespan)


@app.exception_handler(BaseCustomException)
async def base_exception_handler(
    request: Request, exc: BaseCustomException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "detail": str(exc.detail),
        },
    )


for router in routers:
    app.include_router(router)
