from typing import Annotated

from fastapi import Depends

from smoke_health_api.application.services.health_service import HealthService
from smoke_health_api.domain.ports.liveness_read_port import LivenessReadPort
from smoke_health_api.domain.services.liveness_domain_service import LivenessDomainService
from smoke_health_api.infrastructure.adapters.application.liveness_health_service_adapter import (
    LivenessBackedHealthService,
)

_DEFAULT_LIVENESS_READER: LivenessReadPort = LivenessDomainService()


def get_liveness_read_port() -> LivenessReadPort:
    return _DEFAULT_LIVENESS_READER


def get_health_service(
    reader: Annotated[LivenessReadPort, Depends(get_liveness_read_port)],
) -> HealthService:
    return LivenessBackedHealthService(reader)
