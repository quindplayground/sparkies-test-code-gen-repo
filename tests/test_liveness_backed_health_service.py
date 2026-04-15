from unittest.mock import Mock

import pytest

from smoke_health_api.domain.errors import DomainError
from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.domain.models.liveness import Liveness, LivenessId
from smoke_health_api.infrastructure.adapters.application.liveness_health_service_adapter import (
    LivenessBackedHealthService,
)


def test_get_health_returns_ok_when_port_returns_ok_liveness() -> None:
    port = Mock()
    port.read.return_value = Liveness(
        aggregate_id=LivenessId("any"),
        health_status=HealthStatus.ok(),
    )
    service = LivenessBackedHealthService(port)

    assert service.get_health() == HealthStatus.ok()
    port.read.assert_called_once_with()


def test_get_health_propagates_domain_error_from_port() -> None:
    port = Mock()
    port.read.side_effect = DomainError("reader failed")
    service = LivenessBackedHealthService(port)

    with pytest.raises(DomainError, match="reader failed"):
        service.get_health()


def test_get_health_propagates_runtime_error_from_port() -> None:
    port = Mock()
    port.read.side_effect = RuntimeError("boom")
    service = LivenessBackedHealthService(port)

    with pytest.raises(RuntimeError, match="boom"):
        service.get_health()


def test_get_health_invokes_port_on_each_call() -> None:
    port = Mock()
    port.read.return_value = Liveness(
        aggregate_id=LivenessId("any"),
        health_status=HealthStatus.ok(),
    )
    service = LivenessBackedHealthService(port)

    service.get_health()
    service.get_health()

    assert port.read.call_count == 2
