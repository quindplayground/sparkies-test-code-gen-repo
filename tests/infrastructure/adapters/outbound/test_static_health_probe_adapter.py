from smoke_health_api.infrastructure.adapters.outbound.static_health_probe_adapter import (
    StaticHealthProbeAdapter,
)


def test_static_health_probe_adapter_returns_ok() -> None:
    probe = StaticHealthProbeAdapter()
    assert probe.get_health_status().value == "ok"


def test_static_health_probe_adapter_returns_ok_on_repeated_calls() -> None:
    probe = StaticHealthProbeAdapter()
    first = probe.get_health_status()
    second = probe.get_health_status()
    assert first.value == "ok"
    assert second.value == "ok"
    assert first is not second
