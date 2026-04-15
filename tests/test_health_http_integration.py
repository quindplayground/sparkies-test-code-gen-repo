from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from smoke_health_api.app import create_app
from smoke_health_api.application.health_service import HealthService
from smoke_health_api.infrastructure.adapters.outbound.static_health_probe_adapter import (
    StaticHealthProbeAdapter,
)
from smoke_health_api.infrastructure.config.dependencies import get_health_service
from smoke_health_api.infrastructure.entrypoints.http.health_router import health_router


def test_get_health_returns_200_with_ok_status() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_health_response_content_type_is_json() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.headers.get("content-type", "").startswith("application/json")


def test_post_health_is_not_allowed() -> None:
    client = TestClient(create_app())
    response = client.post("/health")
    assert response.status_code == 405


def test_unknown_path_returns_404() -> None:
    client = TestClient(create_app())
    response = client.get("/missing")
    assert response.status_code == 404


def test_health_router_returns_service_payload_with_dependency_override() -> None:
    app = FastAPI()
    app.include_router(health_router)
    mock_service = MagicMock(spec=HealthService)
    mock_service.get_liveness_payload.return_value = {"status": "ok"}
    app.dependency_overrides[get_health_service] = lambda: mock_service

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_service.get_liveness_payload.assert_called_once_with()


def test_health_router_returns_500_when_service_raises() -> None:
    app = FastAPI()
    app.include_router(health_router)
    mock_service = MagicMock(spec=HealthService)
    mock_service.get_liveness_payload.side_effect = RuntimeError("boom")
    app.dependency_overrides[get_health_service] = lambda: mock_service

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/health")

    assert response.status_code == 500


def test_static_health_probe_adapter_returns_ok() -> None:
    probe = StaticHealthProbeAdapter()
    assert probe.get_health_status().to_payload() == {"status": "ok"}


def test_static_health_probe_adapter_returns_ok_on_repeated_calls() -> None:
    probe = StaticHealthProbeAdapter()
    first = probe.get_health_status()
    second = probe.get_health_status()
    assert first.to_payload() == {"status": "ok"}
    assert second.to_payload() == {"status": "ok"}
    assert first is not second
