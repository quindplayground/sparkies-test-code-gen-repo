from smoke_health_api.application.services.health_service import HealthService
from smoke_health_api.application.use_cases.get_health_use_case import (
    GetHealthCommand,
    GetHealthUseCase,
)
from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.domain.ports.liveness_read_port import LivenessReadPort


class LivenessBackedHealthService(HealthService):
    def __init__(self, liveness_reader: LivenessReadPort) -> None:
        self._get_health = GetHealthUseCase(liveness_reader)

    def get_health(self) -> HealthStatus:
        return self._get_health.execute(GetHealthCommand())
