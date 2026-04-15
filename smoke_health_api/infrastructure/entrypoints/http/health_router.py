from typing import Annotated

from fastapi import APIRouter, Depends

from smoke_health_api.application.services.health_service import HealthService
from smoke_health_api.infrastructure.config.container import get_health_service

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def read_health(
    health_service: Annotated[HealthService, Depends(get_health_service)],
) -> dict[str, str]:
    return health_service.get_health().to_public_dict()
