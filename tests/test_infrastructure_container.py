from unittest.mock import Mock

import pytest

from smoke_health_api.domain.errors import DomainError
from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.domain.models.liveness import Liveness, LivenessId
from smoke_health_api.domain.services.liveness_domain_service import LivenessDomainService
from smoke_health_api.infrastructure.adapters.application.liveness_health_service_adapter import (
    LivenessBackedHealthService,
)
from smoke_health_api.infrastructure.config.container import (
    get_health_service,
    get_liveness_read_port,
)


def test_get_liveness_read_port_returns_domain_reader_with_ok_snapshot() -> None:
    reader = get_liveness_read_port()

    assert isinstance(reader, LivenessDomainService)
    snap = reader.read()
    assert snap.health_status == HealthStatus.ok()
    assert snap.aggregate_id == LivenessId("smoke-health-api-process")


def test_get_health_service_wires_liveness_backed_implementation() -> None:
    reader = get_liveness_read_port()
    service = get_health_service(reader)

    assert isinstance(service, LivenessBackedHealthService)
    assert service.get_health() == HealthStatus.ok()


def test_get_health_service_propagates_errors_from_injected_reader() -> None:
    bad_reader = Mock()
    bad_reader.read.side_effect = DomainError("no liveness")
    service = get_health_service(bad_reader)

    with pytest.raises(DomainError, match="no liveness"):
        service.get_health()
