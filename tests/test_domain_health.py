import pytest

from smoke_health_api.domain import (
    HealthReportingDomainService,
    HealthReport,
    HealthStatus,
    InvalidHealthStatusError,
)


class _OkProbe:
    def get_health_status(self) -> HealthStatus:
        return HealthStatus.ok()


def test_health_status_ok_payload() -> None:
    assert HealthStatus.ok().to_payload() == {"status": "ok"}


def test_health_status_rejects_unknown_value() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("degraded")


def test_health_report_delegates_to_status_payload() -> None:
    report = HealthReport(status=HealthStatus.ok())
    assert report.to_http_body() == {"status": "ok"}


def test_domain_service_builds_report_from_probe() -> None:
    service = HealthReportingDomainService(probe=_OkProbe())
    assert service.build_liveness_report().to_http_body() == {"status": "ok"}
