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
            thermal_event=state.ThermalEvent(
                high_voltage_battery_thermal_event_propagation=True
            ),
            power_output=energy.POWER_OUTPUT_STATUS_COLD,
            bms_state_raw=6,
        ),
    )
    assert result == {
        "batteryLevel": 79.1,
        "batteryCapacity": 111.52,
        "batteryTempMin": 21.4,
        "batteryTempMid": 24.2,
        "batteryTempMax": 25.0,
        "batteryHvThermalEvent": "nominal",
        "batteryHvThermalEventPropagation": "detected",
        "batteryPowerOutputStatus": "cold",
        "batteryNeedsLfpCalibration": "false",
        "_bmsStateRaw": 6,
    }


def test_battery_characteristics() -> None:
    """Pack hardware and capacity."""
    result = decode(
        "energy.high_voltage.battery_characteristics",
        energy.BatteryCharacteristics(
            chemistry=energy.BATTERY_CELL_CHEMISTRY_NCA,
            cell_type=energy.BATTERY_CELL_50G,
            module_type=energy.BATTERY_MODULE_TYPE_9M,
            pack_capacity=energy.BATTERY_PACK_CAPACITY_135KWH,
            user_total_kwh=123.82,
            user_max_kwh=123.82,
        ),
    )
    assert result == {
        "batteryCellType": "50g",
        "batteryChemistry": "nca",
        "batteryModuleType": "9m",
        "batteryPackCapacity": "135kwh",
        "batteryCapacity": 123.82,
        "batteryMaxCapacity": 123.82,
    }
