from __future__ import annotations

from dataclasses import dataclass

from smoke_health_api.domain.ports import ServiceHealthProviderPort
from smoke_health_api.domain.services import HealthPublicPayloadService


@dataclass(frozen=True, slots=True)
class GetHealthQuery:
    pass


@dataclass(frozen=True, slots=True)
class HealthCheckResponse:
    status: str

    def to_json_body(self) -> dict[str, str]:
        return {"status": self.status}


class GetHealthUseCase:
    def __init__(self, health_provider: ServiceHealthProviderPort) -> None:
        self._health_provider = health_provider

    def execute(self, query: GetHealthQuery | None = None) -> HealthCheckResponse:
        _ = query
        health = self._health_provider.load()
        body = HealthPublicPayloadService.to_public_body(health)
        return HealthCheckResponse(status=body["status"])
