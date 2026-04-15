def test_fastapi_app_is_importable() -> None:
    from smoke_health_api.main import app

    assert app is not None
