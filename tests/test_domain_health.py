import pytest

from smoke_health_api.domain.exceptions import (
    HealthInvariantViolationError,
    InvalidHealthStatusError,
    InvalidServiceIdentityError,
)
from smoke_health_api.domain.models.aggregates import ServiceHealth
from smoke_health_api.domain.models.entities import ServiceInstance
from smoke_health_api.domain.models.value_objects import HealthStatus
from smoke_health_api.domain.services import HealthPublicPayloadService


def test_health_status_ok() -> None:
    status = HealthStatus.ok()
    assert status.value == "ok"


def test_health_status_rejects_non_ok() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("degraded")


def test_health_status_rejects_empty_string() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("")


def test_health_status_rejects_case_insensitive_ok_alias() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("OK")


def test_service_instance_rejects_blank_id() -> None:
    with pytest.raises(InvalidServiceIdentityError):
        ServiceInstance(instance_id="   ")


def test_service_instance_rejects_empty_string() -> None:
    with pytest.raises(InvalidServiceIdentityError):
        ServiceInstance(instance_id="")


def test_service_instance_accepts_padded_id_but_preserves_literal_value() -> None:
    instance = ServiceInstance(instance_id="  svc-1  ")
    assert instance.instance_id == "  svc-1  "


def test_service_health_live_default_name() -> None:
    health = ServiceHealth.live(None)
    assert health.instance.instance_id == "smoke-health-api"
    assert health.status == HealthStatus.ok()


def test_service_health_live_custom_name() -> None:
    health = ServiceHealth.live("  my-service  ")
    assert health.instance.instance_id == "my-service"


def test_service_health_live_blank_falls_back_to_default() -> None:
    health = ServiceHealth.live("   ")
    assert health.instance.instance_id == "smoke-health-api"


def test_service_health_rejects_non_canonical_status_object() -> None:
    class _NonCanonicalStatus:
        value = "degraded"

    instance = ServiceInstance(instance_id="smoke-health-api")
    with pytest.raises(HealthInvariantViolationError):
        ServiceHealth(instance=instance, status=_NonCanonicalStatus())  # type: ignore[arg-type]


def test_public_payload_matches_contract() -> None:
    health = ServiceHealth.live()
    body = HealthPublicPayloadService.to_public_body(health)
    assert body == {"status": "ok"}
    assert set(body.keys()) == {"status"}


def test_public_payload_reflects_aggregate_status_value() -> None:
    health = ServiceHealth.live("payments")
    assert HealthPublicPayloadService.to_public_body(health)["status"] == health.status.value


def test_public_payload_exposes_only_status_key() -> None:
    health = ServiceHealth.live("internal-billing")
    body = HealthPublicPayloadService.to_public_body(health)
    assert body == {"status": "ok"}
    assert "internal-billing" not in body.values()
