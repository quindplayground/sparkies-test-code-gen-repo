from typing import Protocol

from smoke_health_api.domain.health_status import HealthStatus


class HealthStatusProvider(Protocol):
    def get_health_status(self) -> HealthStatus:
        ...
