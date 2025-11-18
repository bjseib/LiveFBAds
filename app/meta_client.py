"""Meta Graph API client for fetching ad creatives."""
from __future__ import annotations

from typing import Iterable, List

import httpx

from .config import get_settings
from .models import Creative


class MetaAdLibraryClient:
    """Small wrapper around the Meta Ad Library endpoint."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def _build_client(self) -> httpx.Client:
        headers = {}
        if self.settings.meta_access_token:
            headers["Authorization"] = f"Bearer {self.settings.meta_access_token}"
        return httpx.Client(base_url=self.settings.meta_ad_library_endpoint, headers=headers, timeout=10.0)

    def fetch_active_creatives(self, publisher_ids: Iterable[str]) -> List[Creative]:
        """Fetch active creatives for the provided publisher IDs.

        For safety during local development this method returns an empty list when no
        access token is provided. This prevents accidental unauthenticated calls to
        the Meta Graph API while still allowing the application to function with
        cached data.
        """

        publisher_ids = list(publisher_ids)
        if not publisher_ids:
            return []
        if not self.settings.meta_access_token:
            return []

        params = {
            "access_token": self.settings.meta_access_token,
            "search_terms": ",".join(publisher_ids),
            "ad_reached_countries": "US",
            "ad_type": "POLITICAL_AND_ISSUE_ADS",
        }

        creatives: List[Creative] = []
        with self._build_client() as client:
            response = client.get(f"/{self.settings.meta_ad_library_version}/ads_archive", params=params)
            response.raise_for_status()
            payload = response.json()
        for item in payload.get("data", []):
            creatives.append(
                Creative(
                    id=item.get("id", ""),
                    publisher_id=item.get("page_id", ""),
                    snapshot_url=item.get("ad_snapshot_url"),
                    title=item.get("ad_creative_link_title"),
                    body=item.get("ad_creative_body"),
                    call_to_action=item.get("ad_creative_link_caption"),
                    platforms=item.get("publisher_platforms", []),
                    spend=None,
                    currency=None,
                    start_time=None,
                    end_time=None,
                    ad_library_url=item.get("ad_snapshot_url"),
                )
            )
        return creatives
