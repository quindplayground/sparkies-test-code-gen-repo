from __future__ import annotations

from smoke_health_api.domain.ports import ServiceHealthProviderPort
from smoke_health_api.domain.services import HealthPublicPayloadService


class HealthApplicationService:
    def __init__(self, health_provider: ServiceHealthProviderPort) -> None:
        self._health_provider = health_provider

    def get_public_health_body(self) -> dict[str, str]:
        health = self._health_provider.load()
        return HealthPublicPayloadService.to_public_body(health)
