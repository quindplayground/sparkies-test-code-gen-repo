from fastapi import APIRouter, Depends

from smoke_health_api.domain.ports.liveness_health_inbound_port import (
    LivenessHealthInboundPort,
)
from smoke_health_api.infrastructure.config.dependencies import get_liveness_health_port
from smoke_health_api.infrastructure.entrypoints.http.health_response import (
    health_report_to_json_body,
)

health_router = APIRouter(tags=["health"])


@health_router.get("/health")
def read_health(
    port: LivenessHealthInboundPort = Depends(get_liveness_health_port),
) -> dict[str, str]:
    return health_report_to_json_body(port.get_liveness_report())
