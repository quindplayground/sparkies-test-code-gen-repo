from dataclasses import dataclass

from smoke_health_api.domain.models.health_status import HealthStatus


@dataclass(frozen=True)
class HealthReport:
    """Aggregate root for the liveness slice: a single validated status, no secrets."""

    status: HealthStatus

    def __post_init__(self) -> None:
        if not isinstance(self.status, HealthStatus):
            raise TypeError("HealthReport.status must be a HealthStatus instance.")
