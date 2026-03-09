from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str

    # Auth
    api_key: str

    # Ingestion buffer
    buffer_batch_size: int = 100
    buffer_flush_interval_ms: int = 500

    # App
    environment: str = "production"
    debug: bool = False


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
