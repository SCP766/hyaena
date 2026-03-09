from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import get_settings


settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=100,
    max_overflow=50,
    pool_timeout=30,
    pool_recycle=1800,
)
