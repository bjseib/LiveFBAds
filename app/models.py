"""Domain models used by the LiveFBAds application."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Category(BaseModel):
    """Represents a Real Money Gaming category."""

    id: str = Field(..., description="Stable identifier for the category.")
    name: str = Field(..., description="Human readable category name.")


class Publisher(BaseModel):
    """Represents a publisher within a category."""

    id: str = Field(..., description="Stable identifier for the publisher.")
    name: str = Field(..., description="Display name of the publisher.")
    category_ids: List[str] = Field(
        default_factory=list,
        description="Categories that the publisher belongs to.",
    )
    country: str = Field(default="US", description="Two letter country code.")
    status: str = Field(default="active", description="Lifecycle state of the publisher.")
    notes: Optional[str] = Field(default=None, description="Optional compliance notes.")


class Creative(BaseModel):
    """Represents an ad creative fetched from Meta's Ad Library."""

    id: str
    publisher_id: str
    snapshot_url: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    call_to_action: Optional[str] = None
    platforms: List[str] = Field(default_factory=list)
    spend: Optional[float] = None
    currency: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    ad_library_url: Optional[str] = Field(
        default=None,
        description="Deep link to Meta's Ad Library entry.",
    )


class CategorySummary(BaseModel):
    """Response model summarising a category."""

    id: str
    name: str
    publisher_count: int


class PublisherCreateRequest(BaseModel):
    """Payload used for creating new publishers via the admin API."""

    name: str
    category_ids: List[str]
    country: str = "US"
    notes: Optional[str] = None


class PublisherUpdateRequest(BaseModel):
    """Payload for updating publisher metadata."""

    name: Optional[str] = None
    category_ids: Optional[List[str]] = None
    country: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AdminOperationResponse(BaseModel):
    """Standard response returned from admin operations."""

    publisher: Publisher
    message: str
