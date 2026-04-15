from dataclasses import FrozenInstanceError

import pytest

from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.domain.models.liveness import Liveness, LivenessId
from smoke_health_api.domain.services.liveness_domain_service import LivenessDomainService


def test_liveness_domain_service_read() -> None:
    svc = LivenessDomainService()
    snap = svc.read()
    assert isinstance(snap, Liveness)
    assert snap.aggregate_id == LivenessId("smoke-health-api-process")
    assert snap.to_public_dict() == {"status": "ok"}


def test_liveness_id_is_frozen_and_equal_by_value() -> None:
    a = LivenessId("p-1")
    b = LivenessId("p-1")
    c = LivenessId("p-2")

    assert a == b
    assert a != c
    with pytest.raises(FrozenInstanceError):
        a.value = "mutate"  # type: ignore[misc]


def test_liveness_to_public_dict_delegates_to_health_status() -> None:
    live = Liveness(
        aggregate_id=LivenessId("custom"),
        health_status=HealthStatus.ok(),
    )

    assert live.to_public_dict() == {"status": "ok"}


def test_liveness_domain_service_successive_reads_are_independent_instances() -> None:
    svc = LivenessDomainService()
    first = svc.read()
    second = svc.read()

    assert first == second
    assert first is not second
