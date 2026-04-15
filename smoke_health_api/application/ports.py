from typing import Protocol

from smoke_health_api.domain.models.health_status import HealthStatus


class HealthStatusProvider(Protocol):
    def provide(self) -> HealthStatus: ...
