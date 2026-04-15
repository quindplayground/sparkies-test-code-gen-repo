import pytest

from smoke_health_api.application.use_cases.get_health_use_case import (
    GetHealthCommand,
)


def test_get_health_command_instances_are_equal_when_empty() -> None:
    assert GetHealthCommand() == GetHealthCommand()


def test_get_health_command_is_hashable_for_frozen_dataclass() -> None:
    a = GetHealthCommand()
    b = GetHealthCommand()

    assert hash(a) == hash(b)


def test_get_health_command_rejects_extra_fields_at_runtime() -> None:
    with pytest.raises(TypeError):
        GetHealthCommand(extra=True)  # type: ignore[call-arg]
