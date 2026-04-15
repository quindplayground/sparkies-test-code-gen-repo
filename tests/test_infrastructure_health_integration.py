from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from smoke_health_api.bootstrap import create_app
from smoke_health_api.domain.models.aggregates import ServiceHealth
from smoke_health_api.infrastructure.adapters.static_health_provider import (
    StaticServiceHealthProvider,
)
from smoke_health_api.infrastructure.config.container import AppContainer


def test_health_endpoint_returns_contract_json() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_static_health_provider_loads_live_aggregate() -> None:
    provider = StaticServiceHealthProvider()
    health = provider.load()
    assert isinstance(health, ServiceHealth)
    assert health.status.value == "ok"


def test_create_app_uses_injected_container() -> None:
    mock_provider = MagicMock()
    mock_provider.load.return_value = ServiceHealth.live()
    app = create_app(AppContainer(health_provider=mock_provider))
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    mock_provider.load.assert_called_once()
