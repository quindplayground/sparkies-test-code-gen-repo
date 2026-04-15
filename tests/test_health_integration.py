from fastapi.testclient import TestClient

from smoke_health_api.main import create_app


def test_get_health_returns_ok_json() -> None:
    app = create_app()
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
