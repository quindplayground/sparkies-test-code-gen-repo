from __future__ import annotations

from fastapi import APIRouter

from smoke_health_api.application.use_cases.get_health import GetHealthUseCase


def create_health_router(get_health_use_case: GetHealthUseCase) -> APIRouter:
    router = APIRouter(tags=["health"])

    @router.get("/health")
    def read_health() -> dict[str, str]:
        return get_health_use_case.execute().to_json_body()

    return router
