from smoke_health_api.application.health_service import HealthService
from smoke_health_api.application.use_cases.get_liveness_health import (
    GetLivenessHealthUseCase,
)
from smoke_health_api.domain.ports.health_probe_port import HealthProbePort
from smoke_health_api.domain.services.health_reporting_domain_service import (
    HealthReportingDomainService,
)
from smoke_health_api.infrastructure.adapters.outbound.static_health_probe_adapter import (
    StaticHealthProbeAdapter,
)


def create_health_service() -> HealthService:
    probe: HealthProbePort = StaticHealthProbeAdapter()
    domain_service = HealthReportingDomainService(probe)
    use_case = GetLivenessHealthUseCase(domain_service=domain_service)
    return HealthService(liveness_use_case=use_case)
