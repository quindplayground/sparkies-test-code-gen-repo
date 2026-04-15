from unittest.mock import create_autospec

import pytest

from smoke_health_api.application.use_cases.get_liveness_health import (
    GetLivenessHealthUseCase,
)
from smoke_health_api.domain import HealthReport, HealthStatus, InvalidHealthStatusError
from smoke_health_api.domain.services.health_reporting_domain_service import (
    HealthReportingDomainService,
)


def test_use_case_get_liveness_report_happy_path() -> None:
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.return_value = HealthReport(status=HealthStatus.ok())
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    result = use_case.get_liveness_report()

    assert result == HealthReport(status=HealthStatus.ok())
    domain.build_liveness_report.assert_called_once_with()


def test_use_case_each_get_liveness_report_calls_domain_again() -> None:
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.return_value = HealthReport(status=HealthStatus.ok())
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    use_case.get_liveness_report()
    use_case.get_liveness_report()

    assert domain.build_liveness_report.call_count == 2


def test_use_case_propagates_invalid_health_status_error() -> None:
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.side_effect = InvalidHealthStatusError("bad status")
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    with pytest.raises(InvalidHealthStatusError):
        use_case.get_liveness_report()


def test_use_case_propagates_unexpected_errors() -> None:
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.side_effect = RuntimeError("boom")
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    with pytest.raises(RuntimeError, match="boom"):
        use_case.get_liveness_report()


def test_use_case_returns_domain_report_from_domain_service() -> None:
    report = HealthReport(status=HealthStatus.ok())
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.return_value = report
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    assert use_case.get_liveness_report() is report


def test_use_case_get_liveness_report_returns_ok_value() -> None:
    domain = create_autospec(HealthReportingDomainService, instance=True)
    domain.build_liveness_report.return_value = HealthReport(status=HealthStatus.ok())
    use_case = GetLivenessHealthUseCase(domain_service=domain)

    assert use_case.get_liveness_report().status.value == "ok"
