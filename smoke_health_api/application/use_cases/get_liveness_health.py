from dataclasses import dataclass

from smoke_health_api.domain.services.health_reporting_domain_service import (
    HealthReportingDomainService,
)


@dataclass(frozen=True)
class GetLivenessHealthCommand:
    pass


class GetLivenessHealthUseCase:
    def __init__(self, domain_service: HealthReportingDomainService) -> None:
        self._domain_service = domain_service

    def execute(self, _command: GetLivenessHealthCommand) -> dict[str, str]:
        report = self._domain_service.build_liveness_report()
        return report.to_http_body()
