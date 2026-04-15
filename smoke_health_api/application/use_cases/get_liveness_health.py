from smoke_health_api.domain.models.health_report import HealthReport
from smoke_health_api.domain.ports.liveness_health_inbound_port import (
    LivenessHealthInboundPort,
)
from smoke_health_api.domain.services.health_reporting_domain_service import (
    HealthReportingDomainService,
)


class GetLivenessHealthUseCase(LivenessHealthInboundPort):
    def __init__(self, domain_service: HealthReportingDomainService) -> None:
        self._domain_service = domain_service

    def get_liveness_report(self) -> HealthReport:
        return self._domain_service.build_liveness_report()
