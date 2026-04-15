def test_import_package_and_app_factory():
    import smoke_health_api.main as main

    app = main.create_app()
    assert app.title == "smoke-health-api"
