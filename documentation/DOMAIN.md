# Domain layer — smoke-health-api

This service has a **minimal domain**: a single liveness concept, no persistence, no messaging. The domain still follows DDD-style boundaries (value object, aggregate root, port, domain service, domain exception) so the core rules stay testable without HTTP, databases, or the network.

## Bounded context

- **Liveness**: the process is reachable and reports a safe, public health indicator.

## Value objects

| Type | Role | Invariants |
|------|------|------------|
| `HealthStatus` | Canonical string status for the public JSON body | Only allowed value today is `"ok"`; enforced in `__post_init__` |

Factory: `HealthStatus.ok()`. Serialization for HTTP: `to_payload()` → `{"status": "<value>"}`.

## Aggregates

| Aggregate root | Consistency boundary |
|----------------|----------------------|
| `HealthReport` | Wraps exactly one `HealthStatus`; `to_http_body()` delegates to the value object so the public shape stays stable and free of extra fields (no secrets). |

There is no entity with a surrogate identity: the report is fully defined by its status value for this smoke API.

## Ports (domain interfaces)

| Port | Responsibility |
|------|----------------|
| `HealthProbePort` | Supplies the current `HealthStatus` from the environment. Implementations live outside the domain (e.g. infrastructure); the domain only depends on this protocol. |

Method: `get_health_status() -> HealthStatus`.

## Domain service

| Service | Responsibility |
|---------|----------------|
| `HealthReportingDomainService` | Orchestrates liveness: reads from `HealthProbePort` and builds a `HealthReport`. Keeps “how we turn a probe into a public report” in one place if rules grow later. |

## Domain exceptions

| Exception | Meaning |
|-----------|---------|
| `InvalidHealthStatusError` | A status string is not allowed for liveness (subclass of `ValueError`). |

## Business rules (from product requirements)

1. The public health response must include JSON with at least `"status": "ok"` when the process is healthy.
2. Do not expose secrets or credentials in domain types or in payloads built for the health endpoint.

## Dependency rule

Nothing in `smoke_health_api/domain/` imports FastAPI, HTTP clients, SQL, or other infrastructure. Tests can use a small fake object implementing `HealthProbePort` and run without I/O.
