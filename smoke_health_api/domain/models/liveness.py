from dataclasses import dataclass

from smoke_health_api.domain.models.health_status import HealthStatus


@dataclass(frozen=True, slots=True)
class LivenessId:
    """Stable identity for the process liveness aggregate in this bounded context."""

    value: str


@dataclass(frozen=True, slots=True)
class Liveness:
    """Aggregate root: process liveness with a single ``HealthStatus`` invariant."""

    aggregate_id: LivenessId
    health_status: HealthStatus

    def to_public_dict(self) -> dict[str, str]:
        return self.health_status.to_public_dict()
