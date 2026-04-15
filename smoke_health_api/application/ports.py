from typing import Protocol

from smoke_health_api.domain.value_objects import HealthStatus


class HealthStatusSource(Protocol):
    def load(self) -> HealthStatus: ...
