# Domain layer — `smoke-health-api`

This service uses a **minimal DDD-style domain** aligned with the product rule: GET `/health` returns HTTP 200 and JSON containing `"status": "ok"`, without persistence, messaging, or secrets in responses.

## Layout

| Path | Role |
|------|------|
| `smoke_health_api/domain/models/value_objects.py` | Value objects |
| `smoke_health_api/domain/models/entities.py` | Entities (identity) |
| `smoke_health_api/domain/models/aggregates.py` | Aggregate root |
| `smoke_health_api/domain/ports/` | Domain ports (`Protocol`) |
| `smoke_health_api/domain/services.py` | Domain services |
| `smoke_health_api/domain/exceptions.py` | Domain-specific errors |

There are **no** framework imports under `domain/` (no FastAPI, HTTP client, ORM, etc.).

## Value objects

### `HealthStatus`

- Immutable (`frozen` dataclass, `slots=True`).
- Single allowed value for a live process: **`ok`** (see `CANONICAL_LIVE_HEALTH_VALUE`).
- Construction with any other string raises **`InvalidHealthStatusError`**.

## Entity

### `ServiceInstance`

- Represents the **identity** of the logical service instance for health reporting (`instance_id`).
- Empty or whitespace-only ids raise **`InvalidServiceIdentityError`**.

## Aggregate

### `ServiceHealth` (aggregate root)

- Consistency boundary for “what we expose as liveness”.
- Composes `ServiceInstance` + `HealthStatus`.
- Factory **`ServiceHealth.live(service_name=None)`** builds the canonical live snapshot: default name `smoke-health-api` when missing or blank after trim.
- If `status.value` is not the canonical live value, **`HealthInvariantViolationError`** is raised (defense in depth together with `HealthStatus`).

## Domain ports

### `ServiceHealthProviderPort`

- `load() -> ServiceHealth`
- Describes **what** the application needs (a current health snapshot), not **how** it is produced (static value, future probes, etc.). Implementations belong outside the domain (e.g. application or infrastructure adapters).

## Domain services

### `HealthPublicPayloadService`

- Stateless helper: maps `ServiceHealth` to the **public** JSON-shaped payload `dict[str, str]` with exactly the `status` key required by the API contract.
- Keeps transport mappers thin: they should not embed business wording or extra fields that could leak implementation details.

## Exceptions

| Type | Meaning |
|------|---------|
| `DomainError` | Base for domain errors |
| `InvalidHealthStatusError` | Disallowed health label |
| `InvalidServiceIdentityError` | Invalid service id |
| `HealthInvariantViolationError` | Broken health aggregate invariant |

## Key business rules

1. Public liveness status for this product is **`ok`** only (aligned with JSON `"status": "ok"`).
2. Service identity used on the snapshot must be **non-empty** after normalization.
3. Domain code does **not** reference credentials, env secrets, or configurable tokens; nothing in the public payload contract carries secrets.

## Testing

Domain rules are covered by **pure unit tests** (no database, no network) under `tests/test_domain_health.py`.
