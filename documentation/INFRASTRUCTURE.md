# Infrastructure layer (`smoke-health-api`)

This document describes how the **infrastructure** package connects the domain and application layers to the HTTP runtime (FastAPI) for the minimal health check service.

## Scope

There is **no database**, **no message broker**, and **no third-party HTTP clients**. Persistence and messaging adapters are therefore absent by design.

## Layout

```text
smoke_health_api/infrastructure/
├── adapters/                 # Outbound adapters (driven side)
│   └── static_health_provider.py
├── config/                   # Composition / dependency wiring
│   └── container.py
└── entrypoints/http/         # Inbound adapters (driving side)
    └── health_router.py
```

## Persistence adapters

- **Engine / ORM**: none (in-memory domain aggregate only).
- **Schema**: not applicable.

The only data source for health is `ServiceHealth.live()` in the domain, exposed through `StaticServiceHealthProvider.load()`.

## API entry points

| Route    | Method | Response contract                                      |
|----------|--------|--------------------------------------------------------|
| `/health` | `GET`  | `200` with JSON body `{"status": "ok"}` (string values). |

Implementation: `infrastructure.entrypoints.http.health_router.create_health_router` registers the route on a FastAPI `APIRouter` with tag `health`. The handler delegates to `GetHealthUseCase.execute`, which loads the aggregate via the port and maps it through `HealthPublicPayloadService.to_public_body`, then returns `HealthCheckResponse.to_json_body()`.

## External integrations

None (no outbound HTTP, no cloud SDKs, no queues).

## Dependency injection

- **Pattern**: small **composition root** + **factory** for the FastAPI app.
- **`AppContainer`** (`infrastructure.config.container`): immutable dataclass holding a `ServiceHealthProviderPort` implementation. `AppContainer.default()` wires `StaticServiceHealthProvider`.
- **`create_app(container=...)`** (`bootstrap.py`): builds `FastAPI`, resolves `GetHealthUseCase` from the container, and mounts the health router.

Alternative implementations of `ServiceHealthProviderPort` can be injected by passing a custom `AppContainer` into `create_app` (used in tests).

## Design patterns applied

| Component                         | Pattern / role |
|-----------------------------------|----------------|
| `StaticServiceHealthProvider`     | **Adapter** implementing `ServiceHealthProviderPort` (outbound). |
| `create_health_router`            | **Factory** producing a configured inbound HTTP adapter. |
| `AppContainer`                    | **Composition root** fragment: centralizes default adapter choice. |
| `GetHealthUseCase`                | Application **use case** (not infrastructure; orchestrates port + domain mapper). |

## Relation to legacy `smoke_health_api/adapters/`

The skeleton previously placed an empty HTTP router under `adapters/http/`. The wired HTTP surface lives under `infrastructure/entrypoints/http/` per the target layout; the old router module is not used by `create_app()`.
