from __future__ import annotations

from dataclasses import dataclass

from smoke_health_api.domain.errors import InvalidHealthStatusError

_PUBLIC_OK = "ok"


@dataclass(frozen=True, slots=True)
class HealthStatus:
    """Immutable public health indicator; only ``ok`` is allowed for liveness."""

    status: str

    def __post_init__(self) -> None:
        if self.status != _PUBLIC_OK:
            msg = f"Public health status must be {_PUBLIC_OK!r}, got {self.status!r}"
            raise InvalidHealthStatusError(msg)

    @classmethod
    def ok(cls) -> HealthStatus:
        return cls(_PUBLIC_OK)

    def to_public_dict(self) -> dict[str, str]:
        return {"status": self.status}
