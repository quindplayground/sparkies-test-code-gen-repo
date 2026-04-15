# Domain layer — smoke-health-api

This service has a single bounded context: **process liveness** for HTTP smoke checks. There is no persistence or messaging; all rules are pure Python.

## Aggregates

### `Liveness` (aggregate root)

- **Identity**: `LivenessId` (string value, default `"smoke-health-api-process"` for this service).
- **Consistency boundary**: one `HealthStatus` that must satisfy public liveness invariants.
- **Public projection**: `to_public_dict()` delegates to the value object and is the only shape intended for HTTP JSON (`{"status": "ok"}`).

## Value objects

### `HealthStatus`

- Immutable (`frozen` dataclass, `slots=True`).
- **Invariant**: the only allowed public status literal is `"ok"`. Any other value raises `InvalidHealthStatusError` at construction time.
- **Factory**: `HealthStatus.ok()` is the supported constructor for the happy path.
- **Rule alignment**: matches the product rule that `GET /health` must expose `"status": "ok"` without extra sensitive fields.

### `LivenessId`

- Immutable identifier string for the liveness aggregate within this minimal model.

## Domain services

### `LivenessDomainService`

- Implements `LivenessReadPort`.
- Encapsulates how a **healthy** process snapshot is assembled (no I/O, no frameworks).
- Intended to be injected so adapters stay thin and tests stay offline.

## Ports (interfaces)

### `LivenessReadPort`

- `read() -> Liveness`: contract for obtaining the current domain snapshot.
- Application or composition code can depend on this port and supply `LivenessDomainService` (or a test double) without databases or network.

## Domain exceptions

| Type | Meaning |
|------|---------|
| `DomainError` | Base for all domain failures. |
| `InvalidHealthStatusError` | Violation of allowed public health status values. |

## Key business rules

1. Public liveness JSON must include `"status"` with value `"ok"` for the nominal path.
2. No secrets or credentials are modeled in the domain types or payloads.
3. Domain code imports no HTTP or persistence frameworks; external behavior is only described via ports.
