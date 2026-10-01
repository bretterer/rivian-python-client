"""Decoders for `energy.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import energy_pb2

_BATTERY_CELL_TYPE_MAP: Final[dict[int, str]] = {
    1: "50g",
    2: "53g",
    3: "g124",
    4: "lg_4695",
}

_LOW_VOLTAGE_HEALTH_MAP: Final[dict[int, str]] = {
    1: "normal",
    2: "low",
}


@RVMDecoder.register(
    "energy.high_voltage.battery_characteristics", energy_pb2.BatteryCharacteristics
)
def decode_battery_characteristics(
    m: energy_pb2.BatteryCharacteristics,
) -> dict[str, Any]:
    """energy.high_voltage.battery_characteristics — fixed pack hardware info.

    Fields:
        batteryCellType: str
        batteryCapacity: float (kWh)
    """
    result: dict[str, Any] = {
        "batteryCellType": _enum(
            _BATTERY_CELL_TYPE_MAP, _present(m, "cell_type"), what="battery cell type"
        )
    }
    if (v := _present(m, "pack_energy")) is not None:
        result["batteryCapacity"] = round(v, 2)
    return result


@RVMDecoder.register("energy.high_voltage.battery_state", energy_pb2.BatteryState)
def decode_battery_state(m: energy_pb2.BatteryState) -> dict[str, Any]:
    """energy.high_voltage.battery_state — charge, capacity and pack temperatures.

    Fields:
        batteryLevel: float (percent)
        batteryCapacity: float (kWh)
        range: float (km, if present)
        batteryTempMin, batteryTempMid, batteryTempMax: float (°C, if present)
        _bmsStateRaw: int — 4 idle, 5 discharging, 6 charging, others unnamed
    """
    result: dict[str, Any] = {}
    if m.HasField("charge_state"):
        charge_state = m.charge_state
        if (v := _present(charge_state, "soc")) is not None:
            result["batteryLevel"] = round(v, 2)
        if (v := _present(charge_state, "pack_energy")) is not None:
            result["batteryCapacity"] = round(v, 2)
        if (v := _present(charge_state, "range")) is not None:
            result["range"] = round(v, 1)
    if m.HasField("temperatures"):
        temps = m.temperatures
        if (v := _present(temps, "min")) is not None:
            result["batteryTempMin"] = round(v, 1)
        if (v := _present(temps, "mid")) is not None:
            result["batteryTempMid"] = round(v, 1)
        if (v := _present(temps, "max")) is not None:
            result["batteryTempMax"] = round(v, 1)
    if (v := _present(m, "bms_state_raw")) is not None:
        result["_bmsStateRaw"] = v
    return result


@RVMDecoder.register(
    "energy.low_voltage.battery_state", energy_pb2.LowVoltageBatteryState
)
def decode_low_voltage_battery_state(
    m: energy_pb2.LowVoltageBatteryState,
) -> dict[str, Any]:
    """energy.low_voltage.battery_state — 12V battery health.

    Fields:
        twelveVoltBatteryHealth: str
    """
    return {
        "twelveVoltBatteryHealth": _enum(
            _LOW_VOLTAGE_HEALTH_MAP, _present(m, "health"), what="12V battery health"
        )
    }
