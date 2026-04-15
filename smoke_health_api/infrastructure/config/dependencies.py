from smoke_health_api.domain.ports.liveness_health_inbound_port import (
    LivenessHealthInboundPort,
)
from smoke_health_api.infrastructure.config.container import create_liveness_health_inbound_port


def get_liveness_health_port() -> LivenessHealthInboundPort:
    return create_liveness_health_inbound_port()
