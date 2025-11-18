"""Application configuration utilities."""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime settings loaded from environment variables."""

    meta_access_token: str | None = Field(
        default=None,
        description="Meta Graph API access token used for authenticated requests.",
    )
    meta_ad_library_version: str = Field(
        default="v18.0",
        description="Meta Graph API version for Ad Library requests.",
    )
    meta_ad_library_endpoint: str = Field(
        default="https://graph.facebook.com",
        description="Base URL for Meta Graph API requests.",
    )
    default_categories: List[dict] = Field(
        default_factory=list,
        description="Static categories loaded when the repository is initialised.",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()
