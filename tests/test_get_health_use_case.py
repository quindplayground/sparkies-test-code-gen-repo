from unittest.mock import Mock

import pytest

from smoke_health_api.application.use_cases.get_health_use_case import (
    GetHealthCommand,
    GetHealthUseCase,
)
from smoke_health_api.domain.errors import DomainError
from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.domain.models.liveness import Liveness, LivenessId


def test_execute_returns_ok_from_liveness_snapshot() -> None:
    port = Mock()
    port.read.return_value = Liveness(
        aggregate_id=LivenessId("test-process"),
        health_status=HealthStatus.ok(),
    )
    use_case = GetHealthUseCase(port)

    result = use_case.execute(GetHealthCommand())

    assert result == HealthStatus.ok()
    port.read.assert_called_once_with()


def test_execute_invokes_reader_on_each_call() -> None:
    port = Mock()
    port.read.return_value = Liveness(
        aggregate_id=LivenessId("test-process"),
        health_status=HealthStatus.ok(),
    )
    use_case = GetHealthUseCase(port)

    use_case.execute(GetHealthCommand())
    use_case.execute(GetHealthCommand())

    assert port.read.call_count == 2


def test_execute_propagates_domain_errors_from_port() -> None:
    port = Mock()
    port.read.side_effect = DomainError("liveness unavailable")
    use_case = GetHealthUseCase(port)

    with pytest.raises(DomainError, match="liveness unavailable"):
        use_case.execute(GetHealthCommand())


def test_execute_propagates_unexpected_errors_from_port() -> None:
    port = Mock()
    port.read.side_effect = RuntimeError("unexpected")
    use_case = GetHealthUseCase(port)

    with pytest.raises(RuntimeError, match="unexpected"):
        use_case.execute(GetHealthCommand())
