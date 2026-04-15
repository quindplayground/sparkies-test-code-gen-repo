# Infrastructure layer — smoke-health-api

The infrastructure layer connects the **domain port** `HealthProbePort` and the **application** `HealthService` to **FastAPI** (HTTP) and a trivial **outbound probe** implementation. There is **no database**, **no ORM**, and **no messaging**, per product scope.

## Persistence adapters

| Component | Engine / tooling | Schema |
|-----------|------------------|--------|
| *(none)* | N/A | N/A |

This service is intentionally stateless for smoke testing; persistence would belong here if requirements change.

## API entry points (inbound adapters)

| Route | Method | Response contract | Module |
|-------|--------|-------------------|--------|
| `/health` | `GET` | `200` with JSON body `{"status": "ok"}` | `smoke_health_api/infrastructure/entrypoints/http/health_router.py` |

The handler depends on `HealthService` via FastAPI `Depends`, keeping HTTP as a thin driving adapter over the application layer.

## External integrations

| Integration | Client / library | Notes |
|-------------|------------------|-------|
| *(none)* | N/A | No third-party APIs, queues, or side-effectful probes in this build |

The outbound probe adapter returns a fixed `HealthStatus.ok()` without network or disk I/O.

## Dependency injection configuration

| Artifact | Role |
|----------|------|
| `smoke_health_api/infrastructure/config/container.py` | **Factory**: `create_health_service()` builds `StaticHealthProbeAdapter` + `HealthService`. |
| `smoke_health_api/infrastructure/config/dependencies.py` | **FastAPI providers**: `get_health_service()` for `Depends`. |

Wiring path: `create_app()` includes `health_router` → route resolves `HealthService` → `HealthService` uses `HealthReportingDomainService` + `HealthProbePort` implementation.

## Design patterns applied

| Pattern | Where | Purpose |
|---------|--------|---------|
| **Adapter (outbound)** | `StaticHealthProbeAdapter` | Maps the “environment probe” concept to a concrete, testable `HealthProbePort` implementation. |
| **Adapter (inbound)** | `health_router` | Maps HTTP `GET /health` to application `HealthService` without domain or FastAPI types leaking across boundaries unnecessarily. |
| **Factory** | `create_health_service()` | Central composition root for the health slice; single place to swap probe implementations later. |
| **Dependency injection** | FastAPI `Depends(get_health_service)` | Framework-managed resolution of the application service per request (construction is cheap for this API). |
| **Repository** | *(not used)* | Reserved for future persistence; none required today. |
| **Proxy** | *(not used)* | No remote or lazy indirection in scope. |

## Tests

Integration coverage lives under `tests/` (e.g. `TestClient` against `create_app()`, plus direct checks on `StaticHealthProbeAdapter`).
