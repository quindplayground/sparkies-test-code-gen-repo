from abc import ABC, abstractmethod

from smoke_health_api.domain.models.health_status import HealthStatus


class HealthService(ABC):
    @abstractmethod
    def get_health(self) -> HealthStatus: ...
