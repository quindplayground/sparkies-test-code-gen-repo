# Infrastructure layer — smoke-health-api

This document describes how the **infrastructure** package wires the domain and application layers to the HTTP runtime. The product intentionally has **no database, cache, or messaging**; infrastructure is limited to FastAPI entrypoints, a small outbound-style adapter for the application service, and FastAPI dependency injection.

## Layout

```text
smoke_health_api/infrastructure/
├── adapters/
│   └── application/
│       └── liveness_health_service_adapter.py   # Application HealthService implementation
├── config/
│   └── container.py                           # DI providers (FastAPI Depends)
└── entrypoints/
    └── http/
        └── health_router.py                   # GET /health (FastAPI APIRouter)
```

## Persistence adapters

- **Database engine**: none.
- **ORM / query builder**: none.
- **Schema**: none.

The service is fully in-memory; liveness is produced by the domain `LivenessDomainService` (pure Python) behind the `LivenessReadPort` contract.

## API entry points

| Route        | Method | Handler            | Response contract                                      |
|-------------|--------|--------------------|--------------------------------------------------------|
| `/health`   | `GET`  | `read_health`      | JSON object with at least `"status": "ok"` (via `HealthStatus.to_public_dict()`). |

- **Framework**: FastAPI (`APIRouter` with `prefix="/health"` and `GET ""` → `/health`).
- **Composition**: `smoke_health_api.main.create_app()` registers the infrastructure health router on the `FastAPI` instance.

## External integrations

- **Third-party HTTP clients**: none (this service does not call outbound HTTP APIs).
- **Messaging / queues**: none.

## Dependency injection

- **Mechanism**: FastAPI `Depends` callables in `smoke_health_api/infrastructure/config/container.py`.
- **Bindings**:
  - `LivenessReadPort` → default singleton `LivenessDomainService()` (process liveness reader).
  - `HealthService` → `LivenessBackedHealthService` constructed per request with the injected `LivenessReadPort`.

Tests and alternate deployments can override dependencies via `FastAPI.dependency_overrides` without changing domain rules.

## Design patterns applied

| Pattern    | Where | Role |
|-----------|--------|------|
| **Adapter** | `LivenessBackedHealthService` | Adapts `LivenessReadPort` + `Liveness` aggregate to the application `HealthService` contract (`get_health` → `HealthStatus`). |
| **Adapter (inbound)** | `health_router` | Adapts HTTP GET to application service invocation and JSON mapping. |
| **Ports** | Domain / application | `LivenessReadPort` (domain) and `HealthService` (application) remain framework-free; infrastructure implements or drives them. |
| **Composition root** | `main.create_app` | Central place where routers are attached to the ASGI app. |

There is no **Repository** (no persistence), **Proxy** (no remote indirection), or **Factory** type beyond small provider functions used as FastAPI dependencies.

## Backward compatibility

`smoke_health_api.adapters.http.health_router` re-exports the same `router` object from infrastructure for import paths that predate the `infrastructure/` package.
