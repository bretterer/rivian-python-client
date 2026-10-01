"""Tests for the `energy.*` and parked-energy decoders."""

from __future__ import annotations

from rivian.parallax.proto import energy_pb2 as energy

from .helpers import decode


def test_battery_state() -> None:
    """Charge state and min/mid/max pack temperatures."""
    state = energy.BatteryState
    result = decode(
        "energy.high_voltage.battery_state",
        state(
            charge_state=state.ChargeState(soc=79.1, pack_energy=111.52),
            temperatures=state.Temperatures(mid=24.2, max=25.0, min=21.4),
            bms_state_raw=6,
        ),
    )
    assert result == {
        "batteryLevel": 79.1,
        "batteryCapacity": 111.52,
        "batteryTempMin": 21.4,
        "batteryTempMid": 24.2,
        "batteryTempMax": 25.0,
        "_bmsStateRaw": 6,
    }


def test_battery_characteristics() -> None:
    """Cell type and nominal pack energy."""
    result = decode(
        "energy.high_voltage.battery_characteristics",
        energy.BatteryCharacteristics(
            cell_type=energy.BATTERY_CELL_50G, pack_energy=123.82
        ),
    )
    assert result == {"batteryCellType": "50g", "batteryCapacity": 123.82}
