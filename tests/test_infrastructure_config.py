from unittest.mock import MagicMock, patch

import pytest

from smoke_health_api.domain import HealthStatus
from smoke_health_api.infrastructure.config.container import create_liveness_health_inbound_port
from smoke_health_api.infrastructure.config.dependencies import get_liveness_health_port


def test_create_liveness_health_inbound_port_returns_ok_liveness_report() -> None:
    port = create_liveness_health_inbound_port()
    report = port.get_liveness_report()
    assert report.status.value == "ok"


def test_create_liveness_health_inbound_port_builds_fresh_stack_each_call() -> None:
    first = create_liveness_health_inbound_port()
    second = create_liveness_health_inbound_port()
    assert first is not second
    assert first.get_liveness_report().status.value == "ok"
    assert second.get_liveness_report().status.value == "ok"


def test_get_liveness_health_port_matches_container_factory_output() -> None:
    from_container = create_liveness_health_inbound_port()
    from_dependency = get_liveness_health_port()
    assert (
        from_container.get_liveness_report().status.value
        == from_dependency.get_liveness_report().status.value
    )


@patch(
    "smoke_health_api.infrastructure.config.container.StaticHealthProbeAdapter",
)
def test_create_liveness_health_inbound_port_propagates_probe_runtime_error(
    mock_adapter_cls: MagicMock,
) -> None:
    fake_probe = MagicMock()
    fake_probe.get_health_status.side_effect = RuntimeError("probe unavailable")
    mock_adapter_cls.return_value = fake_probe

    port = create_liveness_health_inbound_port()
    with pytest.raises(RuntimeError, match="probe unavailable"):
        port.get_liveness_report()


@patch(
    "smoke_health_api.infrastructure.config.container.StaticHealthProbeAdapter",
)
def test_get_liveness_health_port_propagates_probe_runtime_error(
    mock_adapter_cls: MagicMock,
) -> None:
    fake_probe = MagicMock()
    fake_probe.get_health_status.side_effect = RuntimeError("probe unavailable")
    mock_adapter_cls.return_value = fake_probe

    port = get_liveness_health_port()
    with pytest.raises(RuntimeError, match="probe unavailable"):
        port.get_liveness_report()


@patch(
    "smoke_health_api.infrastructure.config.container.StaticHealthProbeAdapter",
)
def test_create_liveness_health_inbound_port_propagates_invalid_health_status_error(
    mock_adapter_cls: MagicMock,
) -> None:
    from smoke_health_api.domain.exceptions.invalid_health_status_error import (
        InvalidHealthStatusError,
    )

    fake_probe = MagicMock()
    fake_probe.get_health_status.side_effect = InvalidHealthStatusError("bad status")
    mock_adapter_cls.return_value = fake_probe

    port = create_liveness_health_inbound_port()
    with pytest.raises(InvalidHealthStatusError, match="bad status"):
        port.get_liveness_report()


def test_health_status_ok_value_is_stable() -> None:
    assert HealthStatus.ok().value == "ok"
