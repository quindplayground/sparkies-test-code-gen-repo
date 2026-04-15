from dataclasses import dataclass

from smoke_health_api.domain.exceptions.invalid_health_status_error import (
    InvalidHealthStatusError,
)

_ALLOWED_LIVENESS_VALUES: frozenset[str] = frozenset({"ok"})


@dataclass(frozen=True)
class HealthStatus:
    value: str

    def __post_init__(self) -> None:
        if self.value not in _ALLOWED_LIVENESS_VALUES:
            raise InvalidHealthStatusError(
                f"Health status must be one of {sorted(_ALLOWED_LIVENESS_VALUES)}, "
                f"got {self.value!r}."
            )

    @classmethod
    def ok(cls) -> "HealthStatus":
        return cls("ok")
