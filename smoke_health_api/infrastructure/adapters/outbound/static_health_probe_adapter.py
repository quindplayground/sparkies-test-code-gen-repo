from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.domain.ports.health_probe_port import HealthProbePort


class StaticHealthProbeAdapter:
    """Outbound adapter: supplies a fixed liveness status (no I/O)."""

    def get_health_status(self) -> HealthStatus:
        return HealthStatus.ok()
