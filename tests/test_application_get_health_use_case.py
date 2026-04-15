from unittest.mock import MagicMock

import pytest

from smoke_health_api.application.use_cases.get_health import (
    GetHealthQuery,
    GetHealthUseCase,
    HealthCheckResponse,
)
from smoke_health_api.domain.exceptions import DomainError
from smoke_health_api.domain.models.aggregates import ServiceHealth
from smoke_health_api.domain.services import HealthPublicPayloadService


def test_execute_happy_path_returns_contract_response() -> None:
    provider = MagicMock()
    provider.load.return_value = ServiceHealth.live()
    use_case = GetHealthUseCase(provider)

    result = use_case.execute()

    assert isinstance(result, HealthCheckResponse)
    assert result.status == "ok"
    assert result.to_json_body() == {"status": "ok"}
    provider.load.assert_called_once_with()


def test_execute_with_explicit_query_matches_happy_path() -> None:
    provider = MagicMock()
    provider.load.return_value = ServiceHealth.live()
    use_case = GetHealthUseCase(provider)

    assert use_case.execute(GetHealthQuery()).to_json_body() == {"status": "ok"}
    provider.load.assert_called_once_with()


def test_execute_uses_domain_public_payload_mapping() -> None:
    provider = MagicMock()
    provider.load.return_value = ServiceHealth.live("custom-service")
    use_case = GetHealthUseCase(provider)

    result = use_case.execute()
    expected = HealthPublicPayloadService.to_public_body(ServiceHealth.live("custom-service"))

    assert result.to_json_body() == expected


def test_execute_propagates_provider_runtime_errors() -> None:
    provider = MagicMock()
    provider.load.side_effect = RuntimeError("provider unavailable")
    use_case = GetHealthUseCase(provider)

    with pytest.raises(RuntimeError, match="provider unavailable"):
        use_case.execute()


def test_execute_propagates_domain_errors_from_port() -> None:
    provider = MagicMock()
    provider.load.side_effect = DomainError("invariant failed upstream")
    use_case = GetHealthUseCase(provider)

    with pytest.raises(DomainError, match="invariant failed upstream"):
        use_case.execute()
