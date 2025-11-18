"""Application entrypoint for LiveFBAds FastAPI service."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from .api import admin_router, public_router
from .meta_client import MetaAdLibraryClient
from .repository import InMemoryRepository


SEED_PATH = Path(__file__).resolve().parent.parent / "data" / "seed.json"


def create_app() -> FastAPI:
    repository = InMemoryRepository(SEED_PATH)
    app = FastAPI(title="LiveFBAds", description="Live ad creative browser for Real Money Gaming publishers")
    app.state.repository = repository
    app.state.meta_client = MetaAdLibraryClient()

    app.include_router(public_router)
    app.include_router(admin_router)
    return app


app = create_app()
