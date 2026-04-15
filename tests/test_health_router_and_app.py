from fastapi.testclient import TestClient

from smoke_health_api.application.services.health_service import HealthService
from smoke_health_api.domain.errors import DomainError
from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.infrastructure.config.container import get_health_service
from smoke_health_api.main import create_app


def test_post_health_returns_method_not_allowed() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.post("/health")

    assert response.status_code == 405


def test_unknown_route_returns_not_found() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/missing-route")

    assert response.status_code == 404


def test_dependency_override_domain_error_surfaces_as_server_error() -> None:
    class FailingHealthService(HealthService):
        def get_health(self) -> HealthStatus:
            raise DomainError("forced failure")

    app = create_app()
    app.dependency_overrides[get_health_service] = lambda: FailingHealthService()
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/health")

    assert response.status_code == 500
    app.dependency_overrides.clear()


def test_dependency_override_runtime_error_surfaces_as_server_error() -> None:
    class BrokenHealthService(HealthService):
        def get_health(self) -> HealthStatus:
            raise RuntimeError("broken")

    app = create_app()
    app.dependency_overrides[get_health_service] = lambda: BrokenHealthService()
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/health")

    assert response.status_code == 500
    app.dependency_overrides.clear()
