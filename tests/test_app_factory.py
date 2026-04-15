from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from smoke_health_api.app import create_app


def test_create_app_returns_fastapi_instance() -> None:
    app = create_app()
    assert isinstance(app, FastAPI)


def test_create_app_registers_health_route() -> None:
    app = create_app()
    paths = {route.path for route in app.routes if isinstance(route, APIRoute)}
    assert "/health" in paths


def test_create_app_instances_are_independent() -> None:
    first = create_app()
    second = create_app()
    assert first is not second


def test_create_app_serves_health_without_shared_global_state() -> None:
    client_a = TestClient(create_app())
    client_b = TestClient(create_app())
    assert client_a.get("/health").json() == {"status": "ok"}
    assert client_b.get("/health").json() == {"status": "ok"}
