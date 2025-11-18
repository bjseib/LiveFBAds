"""FastAPI routers for public and admin functionality."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status

from .models import (
    AdminOperationResponse,
    CategorySummary,
    Creative,
    Publisher,
    PublisherCreateRequest,
    PublisherUpdateRequest,
)
from .services import AdminService, CategoryService, CreativeService


def get_category_service(request: Request) -> CategoryService:
    return CategoryService(request.app.state.repository)


def get_admin_service(request: Request) -> AdminService:
    return AdminService(request.app.state.repository)


def get_creative_service(request: Request) -> CreativeService:
    return CreativeService(request.app.state.repository, request.app.state.meta_client)


public_router = APIRouter(prefix="/api", tags=["public"])
admin_router = APIRouter(prefix="/api/admin", tags=["admin"])


@public_router.get("/categories", response_model=list[CategorySummary])
async def list_categories(service: CategoryService = Depends(get_category_service)) -> list[CategorySummary]:
    return service.list_category_summaries()


@public_router.get(
    "/categories/{category_id}/publishers",
    response_model=list[Publisher],
)
async def list_publishers_for_category(
    category_id: str,
    request: Request,
) -> list[Publisher]:
    repository = request.app.state.repository
    return repository.list_publishers_by_category(category_id)


@public_router.get(
    "/categories/{category_id}/ads",
    response_model=list[Creative],
)
async def list_ads_for_category(
    category_id: str,
    service: CreativeService = Depends(get_creative_service),
) -> list[Creative]:
    return service.get_cached_creatives_for_category(category_id)


@admin_router.post("/publishers", response_model=AdminOperationResponse, status_code=status.HTTP_201_CREATED)
async def create_publisher(
    payload: PublisherCreateRequest,
    service: AdminService = Depends(get_admin_service),
) -> AdminOperationResponse:
    return service.create_publisher(
        payload.name,
        payload.category_ids,
        country=payload.country,
        notes=payload.notes,
    )


@admin_router.put("/publishers/{publisher_id}", response_model=AdminOperationResponse)
async def update_publisher(
    publisher_id: str,
    payload: PublisherUpdateRequest,
    service: AdminService = Depends(get_admin_service),
) -> AdminOperationResponse:
    try:
        return service.update_publisher(
            publisher_id,
            name=payload.name,
            category_ids=payload.category_ids,
            country=payload.country,
            status=payload.status,
            notes=payload.notes,
        )
    except ValueError as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@admin_router.delete("/publishers/{publisher_id}", response_model=AdminOperationResponse)
async def archive_publisher(
    publisher_id: str,
    service: AdminService = Depends(get_admin_service),
) -> AdminOperationResponse:
    try:
        return service.archive_publisher(publisher_id)
    except ValueError as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
