from typing import Protocol

from smoke_health_api.domain.models.aggregates import ServiceHealth


class ServiceHealthProviderPort(Protocol):
    def load(self) -> ServiceHealth: ...
