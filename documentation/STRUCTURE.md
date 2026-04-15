# Project structure

This document describes the layout of `smoke-health-api` and how folders map to Clean Architecture layers.

## Layout

```text
.
├── documentation/
│   └── STRUCTURE.md          # This file
├── smoke_health_api/         # Installable Python package (project name: smoke-health-api)
│   ├── domain/               # Domain layer
│   ├── application/          # Application layer (use cases, ports)
│   ├── adapters/             # Interface adapters (HTTP, etc.)
│   └── main.py               # ASGI app composition (wiring only)
├── tests/                    # Pytest suite
├── pyproject.toml            # Project metadata and packaging
├── requirements.txt        # Runtime and test dependencies for local/CI installs
└── pytest.ini               # Pytest discovery and paths
```

## Layers

| Path | Layer | Responsibility |
|------|--------|----------------|
| `smoke_health_api/domain/` | Domain | Core types and value objects (e.g. health status). No framework imports. |
| `smoke_health_api/application/` | Application | Application services and `Protocol` ports describing what the app needs from the outside world. |
| `smoke_health_api/adapters/` | Adapters | Framework-specific implementations (FastAPI routers, future clients). |
| `smoke_health_api/main.py` | Composition root | Builds the FastAPI app and registers routers. Keeps orchestration separate from domain rules. |
| `tests/` | Tests | Validates behavior with `pytest` and HTTP clients (e.g. Starlette `TestClient`). |

## Conventions

- **Imports**: Application and domain code must not depend on adapter details beyond declared ports; adapters depend inward on application/domain types.
- **HTTP**: FastAPI routers live under `smoke_health_api/adapters/http/`.
- **Naming**: The distribution name is `smoke-health-api`; the importable package is `smoke_health_api` (PEP 8 module naming).

## Next steps (out of scope for the skeleton)

- Implement `GET /health` on the health router using an application service and domain `HealthStatus`.
- Wire a concrete `HealthService` implementation in `create_app()`.
