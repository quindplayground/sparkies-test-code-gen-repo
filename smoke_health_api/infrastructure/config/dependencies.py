from smoke_health_api.application.health_service import HealthService
from smoke_health_api.infrastructure.config.container import create_health_service


def get_health_service() -> HealthService:
    return create_health_service()
