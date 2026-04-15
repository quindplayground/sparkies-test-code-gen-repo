from smoke_health_api.infrastructure.config.container import create_health_service
from smoke_health_api.infrastructure.config.dependencies import get_health_service


def test_create_health_service_returns_ok_liveness_payload() -> None:
    service = create_health_service()
    assert service.get_liveness_payload() == {"status": "ok"}


def test_create_health_service_builds_fresh_stack_each_call() -> None:
    first = create_health_service()
    second = create_health_service()
    assert first is not second
    assert first.get_liveness_payload() == {"status": "ok"}
    assert second.get_liveness_payload() == {"status": "ok"}


def test_get_health_service_matches_container_factory_output() -> None:
    from_container = create_health_service()
    from_dependency = get_health_service()
    assert from_container.get_liveness_payload() == from_dependency.get_liveness_payload()
