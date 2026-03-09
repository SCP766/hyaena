from fastapi import Security
from fastapi.security import APIKeyHeader
from app.middleware.api_key.exception.api_key_invalid import (
    InvalidAPIKeyException,
)
from app.core.config import get_settings

x_api_key_header = APIKeyHeader(name="x-api-key", scheme_name="x-api-key")
settings = get_settings()


async def verify_x_api_key(
    x_api_key: str = Security(x_api_key_header),
) -> None:
    print(settings)
    if x_api_key != settings.api_key:
        raise InvalidAPIKeyException
