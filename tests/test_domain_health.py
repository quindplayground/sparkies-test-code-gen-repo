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


class _ExplodingProbe:
    def get_health_status(self) -> HealthStatus:
        raise RuntimeError("probe unavailable")


class _InvalidStatusProbe:
    def get_health_status(self) -> HealthStatus:
        raise InvalidHealthStatusError("status rejected by probe")


def test_health_status_ok_payload() -> None:
    assert HealthStatus.ok().to_payload() == {"status": "ok"}


def test_health_status_ok_factory_matches_literal_ok() -> None:
    assert HealthStatus.ok().value == "ok"


def test_health_status_rejects_unknown_value() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("degraded")


def test_health_status_rejects_empty_string() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("")


def test_health_status_rejects_uppercase_ok() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("OK")


def test_health_report_delegates_to_status_payload() -> None:
    report = HealthReport(status=HealthStatus.ok())
    assert report.to_http_body() == {"status": "ok"}


def test_health_report_rejects_non_health_status_status() -> None:
    with pytest.raises(TypeError):
        HealthReport(status="ok")  # type: ignore[arg-type]


def test_health_report_rejects_none_status() -> None:
    with pytest.raises(TypeError):
        HealthReport(status=None)  # type: ignore[arg-type]


def test_invalid_health_status_error_is_value_error_subclass() -> None:
    err = InvalidHealthStatusError("bad")
    assert isinstance(err, ValueError)


def test_domain_service_builds_report_from_probe() -> None:
    service = HealthReportingDomainService(probe=_OkProbe())
    assert service.build_liveness_report().to_http_body() == {"status": "ok"}


def test_domain_service_propagates_probe_runtime_error() -> None:
    service = HealthReportingDomainService(probe=_ExplodingProbe())
    with pytest.raises(RuntimeError, match="probe unavailable"):
        service.build_liveness_report()


def test_domain_service_propagates_invalid_health_status_error_from_probe() -> None:
    service = HealthReportingDomainService(probe=_InvalidStatusProbe())
    with pytest.raises(InvalidHealthStatusError, match="status rejected by probe"):
        service.build_liveness_report()
