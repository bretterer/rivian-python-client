"""Climate and charging command payloads recovered from Android 3.17.0.

Accept the existing VehicleCommand parameter conventions, including the legacy
seat levels (0=off, 2/3/4=low/medium/high). No network activity occurs here.
"""

from __future__ import annotations

import math
from typing import Any

from ..const import VehicleCommand
from .proto import charging_pb2, comfort_pb2 as comfort

_EMPTY_COMMANDS = {
    VehicleCommand.VEHICLE_CABIN_PRECONDITION_ENABLE: "comfort.cabin.enable_preconditioning",
    VehicleCommand.VEHICLE_CABIN_PRECONDITION_DISABLE: "comfort.cabin.disable_preconditioning",
    VehicleCommand.START_CHARGING: "charging.energy.start_charging",
    VehicleCommand.STOP_CHARGING: "charging.energy.stop_charging",
}
_SURFACES = {
    VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT: (
        comfort.SEAT_ROW_1_LEFT,
        comfort.CONDITIONING_HEAT,
    ),
    VehicleCommand.CABIN_HVAC_RIGHT_SEAT_HEAT: (
        comfort.SEAT_ROW_1_RIGHT,
        comfort.CONDITIONING_HEAT,
    ),
    VehicleCommand.CABIN_HVAC_REAR_LEFT_SEAT_HEAT: (
        comfort.SEAT_ROW_2_LEFT,
        comfort.CONDITIONING_HEAT,
    ),
    VehicleCommand.CABIN_HVAC_REAR_RIGHT_SEAT_HEAT: (
        comfort.SEAT_ROW_2_RIGHT,
        comfort.CONDITIONING_HEAT,
    ),
    VehicleCommand.CABIN_HVAC_THIRD_ROW_LEFT_SEAT_HEAT: (
        comfort.SEAT_ROW_3_LEFT,
        comfort.CONDITIONING_HEAT,
    ),
    VehicleCommand.CABIN_HVAC_THIRD_ROW_RIGHT_SEAT_HEAT: (
        comfort.SEAT_ROW_3_RIGHT,
        comfort.CONDITIONING_HEAT,
    ),
    VehicleCommand.CABIN_HVAC_LEFT_SEAT_VENT: (
        comfort.SEAT_ROW_1_LEFT,
        comfort.CONDITIONING_VENT,
    ),
    VehicleCommand.CABIN_HVAC_RIGHT_SEAT_VENT: (
        comfort.SEAT_ROW_1_RIGHT,
        comfort.CONDITIONING_VENT,
    ),
    VehicleCommand.CABIN_HVAC_STEERING_HEAT: (
        comfort.STEERING_WHEEL,
        comfort.CONDITIONING_HEAT,
    ),
}
CONTROL_COMMAND_FEATURES = {
    command: "PVS_COMF_CMD"
    for command in (
        VehicleCommand.VEHICLE_CABIN_PRECONDITION_ENABLE,
        VehicleCommand.VEHICLE_CABIN_PRECONDITION_DISABLE,
        VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP,
        VehicleCommand.CABIN_HVAC_DEFROST_DEFOG,
        *_SURFACES,
    )
}
CONTROL_COMMAND_FEATURES.update(
    dict.fromkeys(
        (
            VehicleCommand.START_CHARGING,
            VehicleCommand.STOP_CHARGING,
            VehicleCommand.CHARGING_LIMITS,
        ),
        "PVS_ENRG_CMD",
    )
)


def encode_control_command(
    command: VehicleCommand,
    params: dict[str, Any] | None = None,
) -> tuple[str, bytes]:
    """Return the RVM and protobuf bytes, rejecting invalid legacy parameters."""
    if command in _EMPTY_COMMANDS:
        return _EMPTY_COMMANDS[command], b""
    params = params or {}
    if command == VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP:
        value = params["HVAC_set_temp"]
        # Preserve the HA LO/HI sentinel values 0 and 63.5 Celsius.
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or not (16 <= value <= 29 or value in (0, 63.5))
        ):
            raise ValueError("Invalid preconditioning temperature")
        return (
            "comfort.cabin.set_preconditioning_temperature",
            comfort.PreconditioningTemperatureCommand(
                temperature_celsius=value
            ).SerializeToString(),
        )
    if command == VehicleCommand.CHARGING_LIMITS:
        value = params["SOC_limit"]
        if type(value) is not int or not 50 <= value <= 100:
            raise ValueError(
                "Charge limit must be an integer percentage between 50 and 100"
            )
        return "charging.energy.set_charge_limit", charging_pb2.ChargeLimitCommand(
            soc_limit=value
        ).SerializeToString()
    if command == VehicleCommand.CABIN_HVAC_DEFROST_DEFOG:
        value = params["level"]
        if type(value) is not int or value not in (0, 1):
            raise ValueError("Defrost level must be 0 or 1")
        level = (
            comfort.DEFROST_COMMAND_COMBINED if value else comfort.DEFROST_COMMAND_OFF
        )
        return "comfort.cabin.set_defrost_defog", comfort.DefrostCommand(
            level=level
        ).SerializeToString()
    if command in _SURFACES:
        value = params["level"]
        wheel = command == VehicleCommand.CABIN_HVAC_STEERING_HEAT
        levels = {
            0: comfort.CONDITIONING_LEVEL_UNSPECIFIED,
            1 if wheel else 2: comfort.CONDITIONING_LEVEL_1,
            2 if wheel else 3: comfort.CONDITIONING_LEVEL_2,
            3 if wheel else 4: comfort.CONDITIONING_LEVEL_3,
        }
        if type(value) is not int or value not in levels:
            raise ValueError("Invalid cabin surface level")
        instance, device = _SURFACES[command]
        payload = comfort.CabinSurfaceCommand(
            instance=instance,
            device=device,
            level=levels[value],
            status=comfort.SURFACE_COMMAND_ON if value else comfort.SURFACE_COMMAND_OFF,
        )
        return "comfort.cabin.set_cabin_surface", payload.SerializeToString()
    raise ValueError("Unsupported climate or charging command")
