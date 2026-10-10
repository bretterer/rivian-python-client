"""Decoders for `energy.*` RVM topics."""

from __future__ import annotations

from typing import Any, Final

from .core import RVMDecoder, _enum, _present
from .proto import energy_pb2

_BATTERY_CELL_TYPE_MAP: Final[dict[int, str]] = {
    energy_pb2.BATTERY_CELL_50G: "50g",
    energy_pb2.BATTERY_CELL_53G: "53g",
    energy_pb2.BATTERY_CELL_G124: "g124",
    energy_pb2.BATTERY_CELL_LG_4695: "lg_4695",
}

_CHEMISTRY_MAP: Final[dict[int, str]] = {
    energy_pb2.BATTERY_CELL_CHEMISTRY_NCA: "nca",
    energy_pb2.BATTERY_CELL_CHEMISTRY_LFP: "lfp",
    energy_pb2.BATTERY_CELL_CHEMISTRY_NMC: "nmc",
}

_MODULE_TYPE_MAP: Final[dict[int, str]] = {
    energy_pb2.BATTERY_MODULE_TYPE_9M: "9m",
    energy_pb2.BATTERY_MODULE_TYPE_1M: "1m",
    energy_pb2.BATTERY_MODULE_TYPE_8M: "8m",
    energy_pb2.BATTERY_MODULE_TYPE_6M: "6m",
    energy_pb2.BATTERY_MODULE_TYPE_11M: "11m",
    energy_pb2.BATTERY_MODULE_TYPE_7M: "7m",
    energy_pb2.BATTERY_MODULE_TYPE_3M: "3m",
    energy_pb2.BATTERY_MODULE_TYPE_10M: "10m",
}

_PACK_CAPACITY_MAP: Final[dict[int, str]] = {
    energy_pb2.BATTERY_PACK_CAPACITY_135KWH: "135kwh",
    energy_pb2.BATTERY_PACK_CAPACITY_150KWH: "150kwh",
    energy_pb2.BATTERY_PACK_CAPACITY_100KWH: "100kwh",
    energy_pb2.BATTERY_PACK_CAPACITY_116KWH: "116kwh",
    energy_pb2.BATTERY_PACK_CAPACITY_108KWH: "108kwh",
    energy_pb2.BATTERY_PACK_CAPACITY_88KWH: "88kwh",
}

_POWER_OUTPUT_MAP: Final[dict[int, str]] = {
    energy_pb2.POWER_OUTPUT_STATUS_NOMINAL: "nominal",
    energy_pb2.POWER_OUTPUT_STATUS_COLD: "cold",
}

_LOW_VOLTAGE_HEALTH_MAP: Final[dict[int, str]] = {
    energy_pb2.LOW_VOLTAGE_NORMAL: "normal",
    energy_pb2.LOW_VOLTAGE_LOW: "low",
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
        batteryChemistry: str | None ("nca" | "lfp" | "nmc")
        batteryModuleType: str | None (e.g. "9m")
        batteryPackCapacity: str | None (e.g. "135kwh")
        batteryUsableCapacity: float (kWh)
        batteryMaxCapacity: float (kWh)
    """
    result: dict[str, Any] = {
        "batteryCellType": _enum(
            _BATTERY_CELL_TYPE_MAP, _present(m, "cell_type"), what="battery cell type"
        ),
        "batteryChemistry": _enum(
            _CHEMISTRY_MAP, m.chemistry or None, what="battery chemistry"
        ),
        "batteryModuleType": _enum(
            _MODULE_TYPE_MAP, m.module_type or None, what="battery module type"
        ),
        "batteryPackCapacity": _enum(
            _PACK_CAPACITY_MAP, m.pack_capacity or None, what="battery pack capacity"
        ),
        "batteryMaxCapacity": round(m.user_max_kwh, 2),
    }
    if (v := _present(m, "user_total_kwh")) is not None:
        result["batteryUsableCapacity"] = round(v, 2)
    return result


@RVMDecoder.register("energy.high_voltage.battery_state", energy_pb2.BatteryState)
def decode_battery_state(m: energy_pb2.BatteryState) -> dict[str, Any]:
    """energy.high_voltage.battery_state — charge, capacity and pack temperatures.

    Fields:
        batteryLevel: float (percent)
        batteryCapacity: float (kWh)
        batteryTempMin, batteryTempMid, batteryTempMax: float (°C; mid is
            the cell average)
        batteryHvThermalEvent, batteryHvThermalEventPropagation: str
            ("nominal" | "detected")
        batteryPowerOutputStatus: str | None ("nominal" | "cold")
        batteryNeedsLfpCalibration: str ("true" | "false")
        _bmsStateRaw: int — 4 idle, 5 discharging, 6 charging, others unnamed
    """
    result: dict[str, Any] = {}
    if m.HasField("charge_state"):
        charge_state = m.charge_state
        result["batteryLevel"] = round(charge_state.soc, 2)
        result["batteryCapacity"] = round(charge_state.pack_energy, 2)
    if m.HasField("temperatures"):
        temps = m.temperatures
        result["batteryTempMin"] = round(temps.min, 1)
        result["batteryTempMid"] = round(temps.mid, 1)
        result["batteryTempMax"] = round(temps.max, 1)
    event = m.thermal_event
    result["batteryHvThermalEvent"] = (
        "detected" if event.high_voltage_battery_thermal_event else "nominal"
    )
    result["batteryHvThermalEventPropagation"] = (
        "detected"
        if event.high_voltage_battery_thermal_event_propagation
        else "nominal"
    )
    result["batteryPowerOutputStatus"] = _enum(
        _POWER_OUTPUT_MAP, m.power_output or None, what="battery power output"
    )
    result["batteryNeedsLfpCalibration"] = "true" if m.requires_calibration else "false"
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
