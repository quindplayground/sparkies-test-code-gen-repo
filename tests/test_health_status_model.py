import pytest

from smoke_health_api.domain.errors import InvalidHealthStatusError
from smoke_health_api.domain.models.health_status import HealthStatus


def test_ok_factory_and_public_dict_happy_path() -> None:
    status = HealthStatus.ok()

    assert status.status == "ok"
    assert status.to_public_dict() == {"status": "ok"}


def test_constructor_rejects_empty_status_string() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("")


def test_constructor_rejects_uppercase_ok_variant() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("OK")


def test_constructor_rejects_whitespace_only_status() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("   ")


def test_constructor_rejects_non_ok_degraded_label() -> None:
    with pytest.raises(InvalidHealthStatusError):
        HealthStatus("degraded")
