from smoke_health_api.bootstrap import create_app


def test_create_app_returns_app() -> None:
    assert create_app() is not None
