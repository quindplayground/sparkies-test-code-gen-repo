# Application use case — health check (`smoke-health-api`)

This document describes the **Get health** application flow: how inbound intent becomes a JSON-safe response while keeping infrastructure out of the use case.

## Location

| Component | Path |
|-----------|------|
| Use case | `smoke_health_api/application/use_cases/get_health.py` |
| HTTP entry | `smoke_health_api/infrastructure/entrypoints/http/health_router.py` |
| Composition | `smoke_health_api/infrastructure/config/container.py`, `smoke_health_api/bootstrap.py` |

## Flow

1. **Input** — `GetHealthUseCase.execute(query: GetHealthQuery | None)`. The query object is reserved for future contextual data; today it is ignored and may be omitted (`None`).
2. **Port call** — The use case calls `ServiceHealthProviderPort.load()` to obtain the domain aggregate `ServiceHealth` (live health snapshot).
3. **Domain mapping** — `HealthPublicPayloadService.to_public_body(health)` builds the minimal public dictionary allowed by product rules (`{"status": "ok"}` for a live service).
4. **Output** — `HealthCheckResponse` wraps the `status` string and exposes `to_json_body()` for the HTTP layer to return as JSON without embedding framework types in the use case return path.

```text
GetHealthQuery (optional) → GetHealthUseCase.execute
  → ServiceHealthProviderPort.load() → ServiceHealth
  → HealthPublicPayloadService.to_public_body → dict
  → HealthCheckResponse → to_json_body() → dict[str, str]
```

## Exceptions

The use case **does not catch** exceptions from the port or domain layer. Typical propagation paths:

| Source | Example | Behaviour |
|--------|---------|-----------|
| Port implementation | `RuntimeError`, I/O failures in a future adapter | Bubbles up; ASGI stack / error handlers decide HTTP mapping. |
| Domain | `DomainError` subclasses (`InvalidHealthStatusError`, `HealthInvariantViolationError`, …) if invalid data is constructed before the use case runs | Bubbles up unchanged. |

Callers (composition root, tests) should inject ports that always return a valid `ServiceHealth` for the live health path, or expect these errors when simulating failure.

## Design notes

- **No HTTP, DB, or messaging** inside the use case; only the domain port and pure domain service.
- **Dependency inversion** — `GetHealthUseCase` depends on `ServiceHealthProviderPort`, not on concrete infrastructure.
