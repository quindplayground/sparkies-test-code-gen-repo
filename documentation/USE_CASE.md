# Use case: Liveness health check

## Purpose

Any client can call `GET /health` to verify the process is alive. The application layer exposes a single use case that produces the JSON body expected by the HTTP adapter, without infrastructure details.

## Flow

1. **Input** — `GetLivenessHealthCommand` (empty today; reserved for future validated inputs such as correlation IDs or feature flags).
2. **Validation** — No application-level validation yet; the command is accepted as-is. Domain rules validate `HealthStatus` when the report is built.
3. **Domain logic** — `GetLivenessHealthUseCase` calls `HealthReportingDomainService.build_liveness_report()`, which uses `HealthProbePort.get_health_status()` and wraps the result in `HealthReport`.
4. **Output** — `dict[str, str]` suitable for JSON serialization, e.g. `{"status": "ok"}`, produced by `HealthReport.to_http_body()` (delegates to `HealthStatus.to_payload()`).

## Primary type

- **Interactor:** `smoke_health_api.application.use_cases.get_liveness_health.GetLivenessHealthUseCase`
- **Command:** `GetLivenessHealthCommand`
- **HTTP façade:** `HealthService.get_liveness_payload()` delegates to the use case for the FastAPI router.

## Exceptions

| Exception | When |
|-----------|------|
| `InvalidHealthStatusError` | Domain rejects a status value outside the allowed liveness set (e.g. not `"ok"`). Propagates to the caller; the HTTP layer may map it later if needed. |
| Other errors | Any failure from the domain service or port implementation propagates unchanged (no swallowing in the use case). |

## Testing

Unit tests mock `HealthReportingDomainService` (or the use case in `HealthService` tests) and cover the happy path, repeated execution, domain error propagation, unexpected errors, and serialization delegation.
