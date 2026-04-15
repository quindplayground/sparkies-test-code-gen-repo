from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from smoke_health_api.app import create_app
from smoke_health_api.domain import HealthReport, HealthStatus
from smoke_health_api.domain.ports.liveness_health_inbound_port import (
    LivenessHealthInboundPort,
)
from smoke_health_api.infrastructure.config.dependencies import get_liveness_health_port
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
    mock_port = MagicMock(spec=LivenessHealthInboundPort)
    mock_port.get_liveness_report.return_value = HealthReport(status=HealthStatus.ok())
    app.dependency_overrides[get_liveness_health_port] = lambda: mock_port

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_port.get_liveness_report.assert_called_once_with()


def test_health_router_returns_500_when_service_raises() -> None:
    app = FastAPI()
    app.include_router(health_router)
    mock_port = MagicMock(spec=LivenessHealthInboundPort)
    mock_port.get_liveness_report.side_effect = RuntimeError("boom")
    app.dependency_overrides[get_liveness_health_port] = lambda: mock_port

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/health")

    assert response.status_code == 500
