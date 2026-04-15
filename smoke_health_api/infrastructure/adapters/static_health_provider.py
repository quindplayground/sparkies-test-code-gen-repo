from __future__ import annotations

from smoke_health_api.domain.models.aggregates import ServiceHealth


class StaticServiceHealthProvider:
    def load(self) -> ServiceHealth:
        return ServiceHealth.live()
