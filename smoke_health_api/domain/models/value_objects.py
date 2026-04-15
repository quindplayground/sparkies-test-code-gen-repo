from __future__ import annotations

from dataclasses import dataclass

from smoke_health_api.domain.exceptions import InvalidHealthStatusError

CANONICAL_LIVE_HEALTH_VALUE = "ok"


@dataclass(frozen=True, slots=True)
class HealthStatus:
    value: str

    def __post_init__(self) -> None:
        if self.value != CANONICAL_LIVE_HEALTH_VALUE:
            msg = (
                f"Health status must be '{CANONICAL_LIVE_HEALTH_VALUE}', "
                f"got {self.value!r}"
            )
            raise InvalidHealthStatusError(msg)

    @classmethod
    def ok(cls) -> HealthStatus:
        return cls(CANONICAL_LIVE_HEALTH_VALUE)
