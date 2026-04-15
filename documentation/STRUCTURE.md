# Project structure

This repository hosts **smoke-health-api**, a minimal FastAPI service. Layout follows a **light Clean Architecture**: domain and application rules stay independent from HTTP details; HTTP is an adapter.

## Layout (relative to repository root)

| Path | Layer | Role |
|------|--------|------|
| `smoke_health_api/` | Composition root | Package boundary; wires adapters to the framework entrypoint. |
| `smoke_health_api/app.py` | Composition | Builds the `FastAPI` application and attaches routers (no domain rules). |
| `smoke_health_api/domain/` | Domain | Core concepts (e.g. health state value types). No framework imports. |
| `smoke_health_api/application/` | Application | Use-case orchestration and ports (`Protocol`) describing what the app needs from the outside. |
| `smoke_health_api/adapters/http/` | Adapter (driving) | HTTP mapping: routes, request/response shapes; depends on FastAPI. |
| `tests/` | Test support | Pytest suite; will use `TestClient` against the ASGI app. |
| `documentation/` | Docs | Human-readable structure and design notes. |

## Dependency rules

- **Domain** does not import application or adapters.
- **Application** may import domain; it defines **ports** (interfaces) for external capabilities.
- **Adapters** implement ports and call into application/domain as needed.
- **`app.py`** only composes the framework and routers.

## Configuration and tooling

- `pyproject.toml` — project metadata, Python `>=3.12`, packaging for `smoke_health_api`.
- `requirements.txt` — runtime and dev dependencies for local installs.
- `pytest.ini` — pytest discovery (`tests/`, `pythonpath`).

## Next implementation steps (out of scope for skeleton)

- Implement `GET /health` on `health_router`, delegating to an application service.
- Add contract tests with `httpx.AsyncClient` or `TestClient` asserting JSON `{ "status": "ok" }`.
