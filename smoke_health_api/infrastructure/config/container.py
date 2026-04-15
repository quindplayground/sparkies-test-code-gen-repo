from smoke_health_api.application.health_service import HealthService
from smoke_health_api.domain.ports.health_probe_port import HealthProbePort
from smoke_health_api.infrastructure.adapters.outbound.static_health_probe_adapter import (
    StaticHealthProbeAdapter,
)


def create_health_service() -> HealthService:
    probe: HealthProbePort = StaticHealthProbeAdapter()
    return HealthService(probe=probe)
