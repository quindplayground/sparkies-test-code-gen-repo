# Project structure (`smoke-health-api`)

This document describes the repository layout and how it maps to a **lightweight Clean Architecture** for the health HTTP service.

## Layout

```text
.
├── documentation/          # Human-facing architecture notes
├── smoke_health_api/       # Installable Python package (application + domain + adapters)
│   ├── adapters/           # Driven side: infrastructure that talks to the outside world
│   │   └── http/           # HTTP adapter (FastAPI routers, request/response mapping)
│   ├── application/      # Use cases / orchestration (application services)
│   ├── domain/             # Core model: entities, value objects, domain rules (no framework imports)
│   ├── bootstrap.py        # Composition root: builds the FastAPI app instance
│   └── main.py             # Package ASGI entrypoint (`app`) for tests and imports
├── tests/                  # Automated tests (pytest; TestClient tests when HTTP is wired)
├── main.py                 # Thin re-export of `app` for `uvicorn main:app`
├── pyproject.toml          # Project metadata, setuptools packaging, optional `dev` extras (pytest, httpx)
├── pytest.ini              # Pytest discovery and paths
├── requirements.txt        # Runtime dependencies (FastAPI + Uvicorn)
└── README.md               # Repository overview
```

## Architectural layers

| Path | Layer | Responsibility |
|------|--------|----------------|
| `smoke_health_api/domain/` | **Domain** | Stable vocabulary and rules (e.g. health status representation). No FastAPI/HTTP imports. |
| `smoke_health_api/application/` | **Application** | Coordinates domain operations for a use case (e.g. assembling the health response payload). |
| `smoke_health_api/adapters/http/` | **Adapter (inbound)** | Translates HTTP requests into application calls and maps results to HTTP responses. |
| `smoke_health_api/bootstrap.py` | **Composition** | `create_app()` factory; wires routers and services when implemented. |
| `smoke_health_api/main.py` | **Runtime entry (package)** | Exposes `app` for imports and tests (`from smoke_health_api.main import app`). |
| `main.py` (repo root) | **Runtime entry (hosting)** | Re-exports `app` for `uvicorn main:app` (or equivalent ASGI hosting). |

## Conventions

- **Package name**: `smoke_health_api` (Python module naming) corresponds to the project name `smoke-health-api` (distribution name in `pyproject.toml`).
- **Language**: Python 3.12, FastAPI + Uvicorn for ASGI, pytest for tests.
- **Secrets**: No credentials or secrets belong in this tree; keep configuration out of source control when it contains sensitive values.

## Skeleton phase (current)

The tree above is the **structural skeleton**: there is no health use-case wiring yet and no `/health` route.

- `smoke_health_api/domain/value_objects.py` defines a named `HealthStatus` placeholder class (no fields or behaviour yet).
- `smoke_health_api/application/ports.py` defines a `HealthStatusSource` `Protocol` for future dependency inversion.
- `smoke_health_api/application/health_service.py` holds an empty `HealthApplicationService` class as a composition hook.
- `smoke_health_api/adapters/http/router.py` exposes an `APIRouter` instance with no routes registered.
- `bootstrap.create_app()` returns a bare `FastAPI` instance; routers are not included until a later task.

## Next implementation steps (out of scope for the skeleton)

1. Flesh out `HealthStatus` (fields, invariants, or a pure factory) and any JSON mapping boundaries.
2. Implement `HealthApplicationService` and inject a `HealthStatusSource` implementation.
3. Add a `/health` route on `adapters.http.router.router` and include that router from `bootstrap.create_app()`.
4. Add pytest coverage using `TestClient` against `create_app()`.
