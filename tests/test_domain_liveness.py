import pytest

from smoke_health_api.domain.errors import InvalidHealthStatusError
from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.domain.models.liveness import Liveness, LivenessId
from smoke_health_api.domain.services.liveness_domain_service import LivenessDomainService


def test_health_status_ok_round_trip() -> None:
    status = HealthStatus.ok()
    assert status.to_public_dict() == {"status": "ok"}


def test_health_status_rejects_non_ok() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("degraded")


def test_liveness_domain_service_read() -> None:
    svc = LivenessDomainService()
    snap = svc.read()
    assert isinstance(snap, Liveness)
    assert snap.aggregate_id == LivenessId("smoke-health-api-process")
    assert snap.to_public_dict() == {"status": "ok"}
