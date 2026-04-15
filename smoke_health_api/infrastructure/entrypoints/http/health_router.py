from __future__ import annotations

from fastapi import APIRouter

from smoke_health_api.application.health_service import HealthApplicationService


def create_health_router(health_service: HealthApplicationService) -> APIRouter:
    router = APIRouter(tags=["health"])

    @router.get("/health")
    def get_health() -> dict[str, str]:
        return health_service.get_public_health_body()

    return router
