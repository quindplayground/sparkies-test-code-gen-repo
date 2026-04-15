from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.domain.models.liveness import Liveness, LivenessId
from smoke_health_api.domain.ports.liveness_read_port import LivenessReadPort

_DEFAULT_LIVENESS_ID = "smoke-health-api-process"


class LivenessDomainService(LivenessReadPort):
    """Pure domain service: builds the canonical process liveness snapshot."""

    def read(self) -> Liveness:
        return Liveness(
            aggregate_id=LivenessId(_DEFAULT_LIVENESS_ID),
            health_status=HealthStatus.ok(),
        )
