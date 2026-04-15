from smoke_health_api.application.use_cases.get_liveness_health import (
    GetLivenessHealthCommand,
    GetLivenessHealthUseCase,
)


class HealthService:
    def __init__(self, liveness_use_case: GetLivenessHealthUseCase) -> None:
        self._liveness_use_case = liveness_use_case

    def get_liveness_payload(self) -> dict[str, str]:
        return self._liveness_use_case.execute(GetLivenessHealthCommand())
