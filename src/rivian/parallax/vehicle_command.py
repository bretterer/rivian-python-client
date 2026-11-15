"""Parallax equivalents of `VehicleCommand`s.

The Rivian app sends a command over Parallax when the vehicle reports its
category's supported feature as AVAILABLE, and as a legacy
`sendVehicleCommand` otherwise.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Final

from ..const import VehicleCommand
from ..exceptions import RivianBadRequestError
from .body import (
    CLOSE_CLOSURES_RVM,
    LOCK_RVM,
    OPEN_CLOSURES_RVM,
    UNLOCK_RVM,
    encode_closures,
    encode_lock,
    encode_unlock,
)
from .charging import (
    SET_CHARGE_LIMIT_RVM,
    START_CHARGING_RVM,
    STOP_CHARGING_RVM,
    encode_charge_limit,
)
from .comfort import (
    DISABLE_PRECONDITIONING_RVM,
    ENABLE_PRECONDITIONING_RVM,
    SET_CABIN_SURFACE_RVM,
    SET_DEFROST_DEFOG_RVM,
    SET_PRECONDITIONING_TEMPERATURE_RVM,
    encode_cabin_surface,
    encode_defrost_defog,
    encode_preconditioning_temperature,
)
from .proto import body_pb2, comfort_pb2
from .security import (
    DISABLE_PANIC_RVM,
    DISABLE_VIDEO_MONITORING_RVM,
    ENABLE_PANIC_RVM,
    ENABLE_VIDEO_MONITORING_RVM,
)

# Legacy `level` param -> level, as the Rivian app maps them; seats have no "1 = on"
_SEAT_LEVELS: Final[dict[int, comfort_pb2.ConditioningLevel]] = {
    0: comfort_pb2.CONDITIONING_LEVEL_UNSPECIFIED,
    2: comfort_pb2.CONDITIONING_LEVEL_1,
    3: comfort_pb2.CONDITIONING_LEVEL_2,
    4: comfort_pb2.CONDITIONING_LEVEL_3,
}
_STEERING_WHEEL_LEVELS: Final[dict[int, comfort_pb2.ConditioningLevel]] = {
    0: comfort_pb2.CONDITIONING_LEVEL_UNSPECIFIED,
    1: comfort_pb2.CONDITIONING_LEVEL_1,
    2: comfort_pb2.CONDITIONING_LEVEL_2,
    3: comfort_pb2.CONDITIONING_LEVEL_3,
}

_Encode = Callable[[dict[str, Any]], bytes]


def _seat(
    surface: comfort_pb2.CabinSurface,
    conditioning: comfort_pb2.ConditioningType = comfort_pb2.CONDITIONING_HEAT,
) -> tuple[str, str, _Encode]:
    return (
        "PVS_COMF_CMD",
        SET_CABIN_SURFACE_RVM,
        lambda p: encode_cabin_surface(surface, conditioning, _SEAT_LEVELS[p["level"]]),
    )


# Command -> (supported feature, RVM, encoder of the `send_vehicle_command` params)
_COMMANDS: Final[dict[str, tuple[str, str, _Encode]]] = {
    VehicleCommand.LOCK_ALL_CLOSURES_FEEDBACK: (
        "PVS_BD_CMD",
        LOCK_RVM,
        lambda _: encode_lock(),
    ),
    VehicleCommand.UNLOCK_ALL_CLOSURES: (
        "PVS_BD_CMD",
        UNLOCK_RVM,
        lambda _: encode_unlock(),
    ),
    VehicleCommand.OPEN_ALL_WINDOWS: (
        "PVS_BD_CMD",
        OPEN_CLOSURES_RVM,
        lambda _: encode_closures(body_pb2.GROUP_WINDOWS),
    ),
    VehicleCommand.CLOSE_ALL_WINDOWS: (
        "PVS_BD_CMD",
        CLOSE_CLOSURES_RVM,
        lambda _: encode_closures(body_pb2.GROUP_WINDOWS),
    ),
    VehicleCommand.OPEN_FRUNK: (
        "PVS_BD_CMD",
        OPEN_CLOSURES_RVM,
        lambda _: encode_closures(body_pb2.FRUNK),
    ),
    VehicleCommand.CLOSE_FRUNK: (
        "PVS_BD_CMD",
        CLOSE_CLOSURES_RVM,
        lambda _: encode_closures(body_pb2.FRUNK),
    ),
    VehicleCommand.OPEN_LIFTGATE_UNLATCH_TAILGATE: (
        "PVS_BD_CMD",
        OPEN_CLOSURES_RVM,
        lambda _: encode_closures(body_pb2.LIFTGATE),
    ),
    VehicleCommand.CLOSE_LIFTGATE: (
        "PVS_BD_CMD",
        CLOSE_CLOSURES_RVM,
        lambda _: encode_closures(body_pb2.LIFTGATE),
    ),
    VehicleCommand.OPEN_CHARGE_PORT_DOOR: (
        "PVS_BD_CMD",
        OPEN_CLOSURES_RVM,
        lambda _: encode_closures(body_pb2.CHARGE_PORT),
    ),
    VehicleCommand.CLOSE_CHARGE_PORT_DOOR: (
        "PVS_BD_CMD",
        CLOSE_CLOSURES_RVM,
        lambda _: encode_closures(body_pb2.CHARGE_PORT),
    ),
    VehicleCommand.PANIC_ON: ("PVS_SEC_CMD", ENABLE_PANIC_RVM, lambda _: b""),
    VehicleCommand.PANIC_OFF: ("PVS_SEC_CMD", DISABLE_PANIC_RVM, lambda _: b""),
    VehicleCommand.ENABLE_GEAR_GUARD_VIDEO: (
        "PVS_SEC_CMD",
        ENABLE_VIDEO_MONITORING_RVM,
        lambda _: b"",
    ),
    VehicleCommand.DISABLE_GEAR_GUARD_VIDEO: (
        "PVS_SEC_CMD",
        DISABLE_VIDEO_MONITORING_RVM,
        lambda _: b"",
    ),
    VehicleCommand.VEHICLE_CABIN_PRECONDITION_ENABLE: (
        "PVS_COMF_CMD",
        ENABLE_PRECONDITIONING_RVM,
        lambda _: b"",
    ),
    VehicleCommand.VEHICLE_CABIN_PRECONDITION_DISABLE: (
        "PVS_COMF_CMD",
        DISABLE_PRECONDITIONING_RVM,
        lambda _: b"",
    ),
    VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP: (
        "PVS_COMF_CMD",
        SET_PRECONDITIONING_TEMPERATURE_RVM,
        lambda p: encode_preconditioning_temperature(float(p["HVAC_set_temp"])),
    ),
    VehicleCommand.CABIN_HVAC_DEFROST_DEFOG: (
        "PVS_COMF_CMD",
        SET_DEFROST_DEFOG_RVM,
        lambda p: encode_defrost_defog(bool(p["level"])),
    ),
    VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT: _seat(comfort_pb2.SEAT_ROW_1_LEFT),
    VehicleCommand.CABIN_HVAC_RIGHT_SEAT_HEAT: _seat(comfort_pb2.SEAT_ROW_1_RIGHT),
    VehicleCommand.CABIN_HVAC_LEFT_SEAT_VENT: _seat(
        comfort_pb2.SEAT_ROW_1_LEFT, comfort_pb2.CONDITIONING_VENT
    ),
    VehicleCommand.CABIN_HVAC_RIGHT_SEAT_VENT: _seat(
        comfort_pb2.SEAT_ROW_1_RIGHT, comfort_pb2.CONDITIONING_VENT
    ),
    VehicleCommand.CABIN_HVAC_REAR_LEFT_SEAT_HEAT: _seat(comfort_pb2.SEAT_ROW_2_LEFT),
    VehicleCommand.CABIN_HVAC_REAR_RIGHT_SEAT_HEAT: _seat(comfort_pb2.SEAT_ROW_2_RIGHT),
    VehicleCommand.CABIN_HVAC_3RD_ROW_REAR_LEFT_SEAT_HEAT: _seat(
        comfort_pb2.SEAT_ROW_3_LEFT
    ),
    VehicleCommand.CABIN_HVAC_3RD_ROW_REAR_RIGHT_SEAT_HEAT: _seat(
        comfort_pb2.SEAT_ROW_3_RIGHT
    ),
    VehicleCommand.CABIN_HVAC_STEERING_HEAT: (
        "PVS_COMF_CMD",
        SET_CABIN_SURFACE_RVM,
        lambda p: encode_cabin_surface(
            comfort_pb2.STEERING_WHEEL,
            comfort_pb2.CONDITIONING_HEAT,
            _STEERING_WHEEL_LEVELS[p["level"]],
        ),
    ),
    VehicleCommand.START_CHARGING: ("PVS_ENRG_CMD", START_CHARGING_RVM, lambda _: b""),
    VehicleCommand.STOP_CHARGING: ("PVS_ENRG_CMD", STOP_CHARGING_RVM, lambda _: b""),
    VehicleCommand.CHARGING_LIMITS: (
        "PVS_ENRG_CMD",
        SET_CHARGE_LIMIT_RVM,
        lambda p: encode_charge_limit(p["SOC_limit"]),
    ),
}


def vehicle_command_feature(command: VehicleCommand | str) -> str | None:
    """Return the supported feature that sends a command over Parallax.

    None if the command has no Parallax equivalent, e.g. honk or wake.
    """
    return entry[0] if (entry := _COMMANDS.get(command)) else None


def encode_vehicle_command(
    command: VehicleCommand | str,
    params: dict[str, Any] | None = None,
) -> tuple[str, bytes]:
    """Return the RVM and payload for a command's Parallax equivalent.

    `params` are those of `send_vehicle_command`, already checked with
    `Rivian.validate_vehicle_command`. Seat level 1 and steering wheel level 4
    have no Parallax equivalent.
    """
    if not (entry := _COMMANDS.get(command)):
        raise RivianBadRequestError(f"{command} has no Parallax equivalent")
    _, rvm, encode = entry
    try:
        return rvm, encode(params or {})
    except KeyError as err:
        raise RivianBadRequestError(
            f"{command} {params} has no Parallax equivalent"
        ) from err
