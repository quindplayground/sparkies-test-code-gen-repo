from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from smoke_health_api.application.use_cases.get_health import (
    GetHealthUseCase,
    HealthCheckResponse,
)
from smoke_health_api.infrastructure.adapters.static_health_provider import (
    StaticServiceHealthProvider,
)
from smoke_health_api.infrastructure.entrypoints.http.health_router import (
    create_health_router,
)


def test_health_router_get_returns_use_case_json_body() -> None:
    use_case = MagicMock(spec=GetHealthUseCase)
    use_case.execute.return_value = HealthCheckResponse(status="ok")
    app = FastAPI()
    app.include_router(create_health_router(use_case))
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    use_case.execute.assert_called_once_with()


def test_health_router_put_returns_method_not_allowed() -> None:
    use_case = MagicMock(spec=GetHealthUseCase)
    use_case.execute.return_value = HealthCheckResponse(status="ok")
    app = FastAPI()
    app.include_router(create_health_router(use_case))
    client = TestClient(app)
    assert client.put("/health").status_code == 405
    use_case.execute.assert_not_called()


def test_health_router_surfaces_use_case_runtime_errors() -> None:
    use_case = MagicMock(spec=GetHealthUseCase)
    use_case.execute.side_effect = RuntimeError("boom")
    app = FastAPI()
    app.include_router(create_health_router(use_case))
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/health")
    assert response.status_code == 500


def test_health_router_with_real_use_case_matches_domain_contract() -> None:
    use_case = GetHealthUseCase(StaticServiceHealthProvider())
    app = FastAPI()
    app.include_router(create_health_router(use_case))
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
