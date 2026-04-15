from __future__ import annotations

from dataclasses import dataclass

from smoke_health_api.domain.exceptions import InvalidServiceIdentityError


def _normalize_service_id(raw: str) -> str:
    cleaned = raw.strip()
    if not cleaned:
        raise InvalidServiceIdentityError("Service instance id must be non-empty")
    return cleaned


@dataclass(frozen=True, slots=True)
class ServiceInstance:
    instance_id: str

    def __post_init__(self) -> None:
        _normalize_service_id(self.instance_id)
