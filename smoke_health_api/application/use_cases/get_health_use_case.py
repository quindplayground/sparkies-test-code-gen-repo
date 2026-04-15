from dataclasses import dataclass

from smoke_health_api.domain.models.health_status import HealthStatus
from smoke_health_api.domain.ports.liveness_read_port import LivenessReadPort


@dataclass(frozen=True, slots=True)
class GetHealthCommand:
    pass


class GetHealthUseCase:
    def __init__(self, liveness_reader: LivenessReadPort) -> None:
        self._liveness_reader = liveness_reader

    def execute(self, command: GetHealthCommand) -> HealthStatus:
        _ = command
        return self._liveness_reader.read().health_status
