from smoke_health_api.main import app


def test_asgi_app_is_created():
    assert app is not None
