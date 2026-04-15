from typing import Protocol

from smoke_health_api.domain.models.liveness import Liveness


class LivenessReadPort(Protocol):
    """Inbound port: obtain the current liveness snapshot without I/O details."""

    def read(self) -> Liveness: ...
