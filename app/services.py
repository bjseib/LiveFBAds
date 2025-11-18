"""Service layer encapsulating business logic."""
from __future__ import annotations

from typing import Iterable, List

from .meta_client import MetaAdLibraryClient
from .models import AdminOperationResponse, CategorySummary, Creative, Publisher
from .repository import InMemoryRepository


class CategoryService:
    """Service for working with categories and related data."""

    def __init__(self, repository: InMemoryRepository) -> None:
        self.repository = repository

    def list_category_summaries(self) -> List[CategorySummary]:
        summaries: List[CategorySummary] = []
        for category in self.repository.list_categories():
            publisher_count = len(self.repository.list_publishers_by_category(category.id))
            summaries.append(
                CategorySummary(
                    id=category.id,
                    name=category.name,
                    publisher_count=publisher_count,
                )
            )
        return summaries


class AdminService:
    """Service used by administrative endpoints to manage publishers."""

    def __init__(self, repository: InMemoryRepository) -> None:
        self.repository = repository

    def create_publisher(self, name: str, category_ids: List[str], country: str = "US", notes: str | None = None) -> AdminOperationResponse:
        publisher_id = self.repository.generate_publisher_id()
        publisher = Publisher(
            id=publisher_id,
            name=name,
            category_ids=category_ids,
            country=country,
            notes=notes,
        )
        publisher = self.repository.upsert_publisher(publisher)
        return AdminOperationResponse(publisher=publisher, message="Publisher created")

    def update_publisher(
        self,
        publisher_id: str,
        *,
        name: str | None = None,
        category_ids: List[str] | None = None,
        country: str | None = None,
        status: str | None = None,
        notes: str | None = None,
    ) -> AdminOperationResponse:
        publisher = self.repository.get_publisher(publisher_id)
        if not publisher:
            raise ValueError("Publisher not found")
        if name is not None:
            publisher.name = name
        if category_ids is not None:
            publisher.category_ids = category_ids
        if country is not None:
            publisher.country = country
        if status is not None:
            publisher.status = status
        if notes is not None:
            publisher.notes = notes
        publisher = self.repository.upsert_publisher(publisher)
        return AdminOperationResponse(publisher=publisher, message="Publisher updated")

    def archive_publisher(self, publisher_id: str) -> AdminOperationResponse:
        publisher = self.repository.archive_publisher(publisher_id)
        if not publisher:
            raise ValueError("Publisher not found")
        return AdminOperationResponse(publisher=publisher, message="Publisher archived")


class CreativeService:
    """Service responsible for retrieving creatives for display."""

    def __init__(self, repository: InMemoryRepository, meta_client: MetaAdLibraryClient | None = None) -> None:
        self.repository = repository
        self.meta_client = meta_client or MetaAdLibraryClient()

    def get_cached_creatives_for_category(self, category_id: str) -> List[Creative]:
        return self.repository.list_creatives_by_category(category_id)

    def refresh_creatives_for_publishers(self, publisher_ids: Iterable[str]) -> List[Creative]:
        creatives = self.meta_client.fetch_active_creatives(publisher_ids)
        for creative in creatives:
            self.repository.upsert_creative(creative)
        return creatives
