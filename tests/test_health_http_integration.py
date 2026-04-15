from fastapi.testclient import TestClient

from smoke_health_api.app import create_app


def test_get_health_returns_200_with_ok_status() -> None:
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_static_health_probe_adapter_returns_ok() -> None:
    from smoke_health_api.infrastructure.adapters.outbound.static_health_probe_adapter import (
        StaticHealthProbeAdapter,
    )

    probe = StaticHealthProbeAdapter()
    assert probe.get_health_status().to_payload() == {"status": "ok"}
