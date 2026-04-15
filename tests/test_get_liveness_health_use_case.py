from unittest.mock import MagicMock, create_autospec

import pytest

from smoke_health_api.application.health_service import HealthService
from smoke_health_api.application.use_cases.get_liveness_health import (
    GetLivenessHealthCommand,
    GetLivenessHealthUseCase,
)
from smoke_health_api.domain import HealthReport, HealthStatus, InvalidHealthStatusError
from smoke_health_api.domain.services.health_reporting_domain_service import (
    HealthReportingDomainService,
)


def test_use_case_execute_happy_path() -> None:
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.return_value = HealthReport(status=HealthStatus.ok())
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    result = use_case.execute(GetLivenessHealthCommand())

    assert result == {"status": "ok"}
    domain.build_liveness_report.assert_called_once_with()


def test_use_case_each_execute_calls_domain_again() -> None:
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.return_value = HealthReport(status=HealthStatus.ok())
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    use_case.execute(GetLivenessHealthCommand())
    use_case.execute(GetLivenessHealthCommand())

    assert domain.build_liveness_report.call_count == 2


def test_use_case_propagates_invalid_health_status_error() -> None:
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.side_effect = InvalidHealthStatusError("bad status")
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    with pytest.raises(InvalidHealthStatusError):
        use_case.execute(GetLivenessHealthCommand())


def test_use_case_propagates_unexpected_errors() -> None:
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.side_effect = RuntimeError("boom")
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    with pytest.raises(RuntimeError, match="boom"):
        use_case.execute(GetLivenessHealthCommand())


def test_use_case_returns_serialized_report_from_domain() -> None:
    report = MagicMock()
    report.to_http_body.return_value = {"status": "ok"}
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.return_value = report
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    assert use_case.execute(GetLivenessHealthCommand()) == {"status": "ok"}
    report.to_http_body.assert_called_once_with()


def test_health_service_delegates_to_use_case() -> None:
    use_case = create_autospec(GetLivenessHealthUseCase, instance=True)
    use_case.execute.return_value = {"status": "ok"}
    service = HealthService(liveness_use_case=use_case)

    assert service.get_liveness_payload() == {"status": "ok"}
    use_case.execute.assert_called_once()
    assert isinstance(use_case.execute.call_args[0][0], GetLivenessHealthCommand)
