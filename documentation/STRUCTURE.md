# Project structure

This repository hosts **smoke-health-api**, a minimal FastAPI service used for smoke and end-to-end checks. The layout follows a **lightweight Clean Architecture**: domain rules stay isolated, application services orchestrate use cases, and HTTP adapters translate requests and responses.

## Top-level layout

| Path | Role |
|------|------|
| `src/smoke_health_api/` | Installable Python package (application code). |
| `tests/` | Pytest suite; currently contains a minimal import smoke test and will host `TestClient` checks later. |
| `documentation/` | Human-oriented technical notes (this file). |
| `pyproject.toml` | Project metadata, packaging, and tool defaults. |
| `requirements.txt` | Pinned-style dependency listing for local installs and CI. |
| `pytest.ini` | Pytest discovery paths and `PYTHONPATH` for the `src` layout. |

## Package layers (`src/smoke_health_api/`)

| Directory / module | Architectural layer | Purpose |
|----------------------|---------------------|---------|
| `domain/` | **Domain** | Core concepts and rules (e.g. health status value types) with no framework imports. |
| `application/` | **Application** | Use-case services that coordinate domain objects without knowing HTTP details. |
| `adapters/http/` | **Driving adapter (HTTP)** | FastAPI routers, request/response mapping, and other web-facing glue. |
| `main.py` | **Composition root (minimal)** | Wires the ASGI `FastAPI` application; later imports routers and dependencies. |

## Dependency direction

- `adapters` → may depend on `application` and shared types from `domain`.
- `application` → depends on `domain` only (no FastAPI imports).
- `domain` → no inward dependencies on other layers.

This keeps `/health` behavior testable from the application layer while keeping HTTP specifics in `adapters/http`.
