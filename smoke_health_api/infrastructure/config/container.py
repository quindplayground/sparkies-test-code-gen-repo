from __future__ import annotations

from dataclasses import dataclass

from smoke_health_api.application.use_cases.get_health import GetHealthUseCase
from smoke_health_api.domain.ports import ServiceHealthProviderPort
from smoke_health_api.infrastructure.adapters.static_health_provider import (
    StaticServiceHealthProvider,
)


@dataclass(frozen=True, slots=True)
class AppContainer:
    health_provider: ServiceHealthProviderPort

    @classmethod
    def default(cls) -> AppContainer:
        return cls(health_provider=StaticServiceHealthProvider())

    def build_get_health_use_case(self) -> GetHealthUseCase:
        return GetHealthUseCase(self.health_provider)
