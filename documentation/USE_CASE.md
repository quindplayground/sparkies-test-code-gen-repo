# Application use case: health check

## Purpose

Allow any client to verify that the `smoke-health-api` process is alive by resolving the canonical public health status from the current liveness snapshot.

## Flow

1. **Input** — `GetHealthCommand` (application command object; currently carries no fields and exists for a stable, extensible boundary).
2. **Validation** — No application-level validation beyond constructing a `GetHealthUseCase` with a `LivenessReadPort` implementation. Domain invariants are enforced when building `HealthStatus` and `Liveness` values inside the domain layer.
3. **Domain logic** — The use case calls `LivenessReadPort.read()` to obtain a `Liveness` aggregate snapshot, then returns its `health_status` (`HealthStatus`).
4. **Output** — `HealthStatus` (immutable value object). The HTTP adapter serializes it with `HealthStatus.to_public_dict()` as `{"status": "ok"}`.

## Primary type

- `GetHealthUseCase` in `smoke_health_api.application.use_cases.get_health_use_case`

## Exceptions

| Situation | Behavior |
|-----------|----------|
| `LivenessReadPort.read()` raises `DomainError` (or subclass) | Propagates unchanged to the caller. |
| `LivenessReadPort.read()` raises any other exception | Propagates unchanged (no swallowing or mapping in the use case). |
| Invalid `HealthStatus` when constructing domain values | Raised as `InvalidHealthStatusError` inside the domain model if violated; not expected for the default liveness path. |

## Wiring

- Infrastructure composes `GetHealthUseCase` with the configured `LivenessReadPort` and exposes `HealthService.get_health()` via `LivenessBackedHealthService` for FastAPI dependency injection.
