from unittest.mock import MagicMock

from smoke_health_api.application.use_cases.get_health import GetHealthUseCase
from smoke_health_api.domain.models.aggregates import ServiceHealth
from smoke_health_api.infrastructure.adapters.static_health_provider import (
    StaticServiceHealthProvider,
)
from smoke_health_api.infrastructure.config.container import AppContainer


def test_default_container_uses_static_health_provider() -> None:
    container = AppContainer.default()
    assert isinstance(container.health_provider, StaticServiceHealthProvider)


def test_build_get_health_use_case_returns_executable_interactor() -> None:
    container = AppContainer.default()
    use_case = container.build_get_health_use_case()
    assert isinstance(use_case, GetHealthUseCase)
    assert use_case.execute().to_json_body() == {"status": "ok"}


def test_build_get_health_use_case_respects_custom_provider() -> None:
    mock_provider = MagicMock()
    mock_provider.load.return_value = ServiceHealth.live("edge-svc")
    container = AppContainer(health_provider=mock_provider)
    use_case = container.build_get_health_use_case()
    assert use_case.execute().to_json_body() == {"status": "ok"}
    mock_provider.load.assert_called_once()
