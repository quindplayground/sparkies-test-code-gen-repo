from fastapi import APIRouter, Depends

from smoke_health_api.application.health_service import HealthService
from smoke_health_api.infrastructure.config.dependencies import get_health_service

health_router = APIRouter(tags=["health"])


@health_router.get("/health")
def read_health(
    service: HealthService = Depends(get_health_service),
) -> dict[str, str]:
    return service.get_liveness_payload()
