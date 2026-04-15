from typing import Protocol

from smoke_health_api.domain.models.health_report import HealthReport


class LivenessHealthInboundPort(Protocol):
    def get_liveness_report(self) -> HealthReport:
        ...
