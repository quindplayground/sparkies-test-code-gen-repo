from typing import Protocol

from smoke_health_api.domain.models.health_status import HealthStatus


class HealthProbePort(Protocol):
    def get_health_status(self) -> HealthStatus:
        ...
