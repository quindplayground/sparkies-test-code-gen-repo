from smoke_health_api.domain.ports.health_probe_port import HealthProbePort
from smoke_health_api.domain.services.health_reporting_domain_service import (
    HealthReportingDomainService,
)


class HealthService:
    def __init__(self, probe: HealthProbePort) -> None:
        self._reporting = HealthReportingDomainService(probe)

    def get_liveness_payload(self) -> dict[str, str]:
        return self._reporting.build_liveness_report().to_http_body()
