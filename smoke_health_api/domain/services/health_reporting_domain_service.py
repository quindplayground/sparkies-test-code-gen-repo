from smoke_health_api.domain.models.health_report import HealthReport
from smoke_health_api.domain.ports.health_probe_port import HealthProbePort


class HealthReportingDomainService:
    def __init__(self, probe: HealthProbePort) -> None:
        self._probe = probe

    def build_liveness_report(self) -> HealthReport:
        status = self._probe.get_health_status()
        return HealthReport(status=status)
