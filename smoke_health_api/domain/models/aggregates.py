from __future__ import annotations

from dataclasses import dataclass

from smoke_health_api.domain.exceptions import HealthInvariantViolationError
from smoke_health_api.domain.models.entities import ServiceInstance
from smoke_health_api.domain.models.value_objects import (
    CANONICAL_LIVE_HEALTH_VALUE,
    HealthStatus,
)

_DEFAULT_SERVICE_NAME = "smoke-health-api"


@dataclass(frozen=True, slots=True)
class ServiceHealth:
    instance: ServiceInstance
    status: HealthStatus

    def __post_init__(self) -> None:
        if self.status.value != CANONICAL_LIVE_HEALTH_VALUE:
            raise HealthInvariantViolationError(
                "Live aggregate must carry the canonical OK status"
            )

    @classmethod
    def live(cls, service_name: str | None = None) -> ServiceHealth:
        label = (service_name or _DEFAULT_SERVICE_NAME).strip() or _DEFAULT_SERVICE_NAME
        return cls(instance=ServiceInstance(instance_id=label), status=HealthStatus.ok())
