"""Repository layer for categories, publishers, and creatives."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .models import Category, Creative, Publisher


class InMemoryRepository:
    """Simple in-memory repository backed by JSON seed data."""

    def __init__(self, seed_path: Optional[Path] = None):
        self._categories: Dict[str, Category] = {}
        self._publishers: Dict[str, Publisher] = {}
        self._creatives: Dict[str, Creative] = {}
        if seed_path and seed_path.exists():
            self.load_seed(seed_path)

    # ------------------------------------------------------------------
    # Seed loading
    # ------------------------------------------------------------------
    def load_seed(self, seed_path: Path) -> None:
        """Load repository state from the provided JSON seed file."""

        import json

        raw = json.loads(seed_path.read_text())
        for category in raw.get("categories", []):
            self.upsert_category(Category(**category))
        for publisher in raw.get("publishers", []):
            self.upsert_publisher(Publisher(**publisher))
        for creative in raw.get("creatives", []):
            self.upsert_creative(Creative(**creative))

    # ------------------------------------------------------------------
    # Category operations
    # ------------------------------------------------------------------
    def upsert_category(self, category: Category) -> None:
        self._categories[category.id] = category

    def list_categories(self) -> List[Category]:
        return list(self._categories.values())

    # ------------------------------------------------------------------
    # Publisher operations
    # ------------------------------------------------------------------
    def upsert_publisher(self, publisher: Publisher) -> Publisher:
        self._publishers[publisher.id] = publisher
        return publisher

    def generate_publisher_id(self) -> str:
        return f"pub_{len(self._publishers) + 1:04d}"

    def get_publisher(self, publisher_id: str) -> Optional[Publisher]:
        return self._publishers.get(publisher_id)

    def list_publishers(self, *, include_inactive: bool = False) -> List[Publisher]:
        if include_inactive:
            return list(self._publishers.values())
        return [p for p in self._publishers.values() if p.status == "active"]

    def list_publishers_by_category(self, category_id: str) -> List[Publisher]:
        return [
            publisher
            for publisher in self.list_publishers()
            if category_id in publisher.category_ids
        ]

    def archive_publisher(self, publisher_id: str) -> Optional[Publisher]:
        publisher = self._publishers.get(publisher_id)
        if publisher:
            publisher.status = "inactive"
            self._publishers[publisher_id] = publisher
        return publisher

    # ------------------------------------------------------------------
    # Creative operations
    # ------------------------------------------------------------------
    def upsert_creative(self, creative: Creative) -> None:
        self._creatives[creative.id] = creative

    def list_creatives_for_publishers(self, publisher_ids: Iterable[str]) -> List[Creative]:
        publisher_set = set(publisher_ids)
        return [
            creative
            for creative in self._creatives.values()
            if creative.publisher_id in publisher_set
        ]

    def list_creatives_by_category(self, category_id: str) -> List[Creative]:
        publisher_ids = [p.id for p in self.list_publishers_by_category(category_id)]
        return self.list_creatives_for_publishers(publisher_ids)

    def creatives_grouped_by_publisher(self, publisher_ids: Iterable[str]) -> Dict[str, List[Creative]]:
        grouped: Dict[str, List[Creative]] = defaultdict(list)
        for creative in self.list_creatives_for_publishers(publisher_ids):
            grouped[creative.publisher_id].append(creative)
        return grouped
