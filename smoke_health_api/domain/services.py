from smoke_health_api.domain.models.aggregates import ServiceHealth


class HealthPublicPayloadService:
    @staticmethod
    def to_public_body(health: ServiceHealth) -> dict[str, str]:
        return {"status": health.status.value}
