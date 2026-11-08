"""Parallax equivalents of `VehicleCommand`s.

The Rivian app sends a command over Parallax when the vehicle reports the
supported feature for the command's category as AVAILABLE, and as a legacy
`sendVehicleCommand` otherwise.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from ..const import VehicleCommand
from ..exceptions import RivianBadRequestError
from .body import LOCK_RVM, UNLOCK_RVM, encode_unlock
from .proto import body_pb2, charging_pb2, comfort_pb2

_Build = Callable[[dict[str, Any]], bytes]

_BODY = "PVS_BD_CMD"
_LIFTGATE = "LIFTGATE_CMD"
_COMFORT = "PVS_COMF_CMD"
_ENERGY = "PVS_ENRG_CMD"
_SECURITY = "PVS_SEC_CMD"

_Level = comfort_pb2.ConditioningLevel
_OFF, _LOW, _MEDIUM, _HIGH = (
    comfort_pb2.CONDITIONING_LEVEL_UNSPECIFIED,
    comfort_pb2.CONDITIONING_LEVEL_1,
    comfort_pb2.CONDITIONING_LEVEL_2,
    comfort_pb2.CONDITIONING_LEVEL_3,
)

_VENT = comfort_pb2.CONDITIONING_VENT

# Legacy `level` param -> level, as the Rivian app maps them; seats have no "1 = on"
_SEAT_LEVELS: dict[int, _Level] = {0: _OFF, 2: _LOW, 3: _MEDIUM, 4: _HIGH}
_WHEEL_LEVELS: dict[int, _Level] = {0: _OFF, 1: _LOW, 2: _MEDIUM, 3: _HIGH}


def _empty(params: dict[str, Any]) -> bytes:
    return b""


def _closure(closure: body_pb2.ClosureId) -> _Build:
    def build(params: dict[str, Any]) -> bytes:
        return body_pb2.ClosuresRequest(closures=[closure]).SerializeToString()

    return build


def _unlock(params: dict[str, Any]) -> bytes:
    return encode_unlock()


def _surface(
    surface: comfort_pb2.CabinSurface,
    type_: comfort_pb2.ConditioningType,
    levels: dict[int, _Level],
) -> _Build:
    def build(params: dict[str, Any]) -> bytes:
        if (level := levels.get(params.get("level", -1))) is None:
            raise RivianBadRequestError(f"Level must be one of {list(levels)}")
        return comfort_pb2.CabinSurfaceRequest(
            surface=surface,
            level=level,
            status=comfort_pb2.CABIN_SURFACE_ON
            if level
            else comfort_pb2.CABIN_SURFACE_OFF,
            type=type_,
        ).SerializeToString()

    return build


def _defrost(params: dict[str, Any]) -> bytes:
    status = (
        comfort_pb2.DEFROST_DEFOG_DEFROST
        if params.get("level")
        else comfort_pb2.DEFROST_OFF
    )
    return comfort_pb2.DefrostDefogRequest(status=status).SerializeToString()


def _temperature(params: dict[str, Any]) -> bytes:
    temp = params.get("HVAC_set_temp")
    if not (isinstance(temp, (int, float)) and (16 <= temp <= 29 or temp in (0, 63.5))):
        raise RivianBadRequestError(
            "Temperature must be between 16 and 29 or 0/63.5 for LO/HI"
        )
    return comfort_pb2.PreconditioningTemperatureRequest(
        temperature=temp
    ).SerializeToString()


def _charge_limit(params: dict[str, Any]) -> bytes:
    limit = params.get("SOC_limit")
    if not (isinstance(limit, int) and 50 <= limit <= 100):
        raise RivianBadRequestError("Charging limit must be between 50 and 100")
    return charging_pb2.ChargeLimitRequest(limit=limit).SerializeToString()


def _seat(
    surface: comfort_pb2.CabinSurface,
    type_: comfort_pb2.ConditioningType = comfort_pb2.CONDITIONING_HEAT,
) -> tuple[str, str, _Build]:
    return (
        _COMFORT,
        "comfort.cabin.set_cabin_surface",
        _surface(surface, type_, _SEAT_LEVELS),
    )


_COMMANDS: dict[str, tuple[str, str, _Build]] = {
    VehicleCommand.LOCK_ALL_CLOSURES_FEEDBACK: (_BODY, LOCK_RVM, _empty),
    VehicleCommand.UNLOCK_ALL_CLOSURES: (_BODY, UNLOCK_RVM, _unlock),
    VehicleCommand.OPEN_ALL_WINDOWS: (
        _BODY,
        "body.closures.open",
        _closure(body_pb2.GROUP_WINDOWS),
    ),
    VehicleCommand.CLOSE_ALL_WINDOWS: (
        _BODY,
        "body.closures.close",
        _closure(body_pb2.GROUP_WINDOWS),
    ),
    VehicleCommand.OPEN_FRUNK: (_BODY, "body.closures.open", _closure(body_pb2.FRUNK)),
    VehicleCommand.CLOSE_FRUNK: (
        _BODY,
        "body.closures.close",
        _closure(body_pb2.FRUNK),
    ),
    # Vehicles without LIFTGATE_CMD, e.g. an R1T's tailgate, keep the old command
    VehicleCommand.OPEN_LIFTGATE_UNLATCH_TAILGATE: (
        _LIFTGATE,
        "body.closures.open",
        _closure(body_pb2.LIFTGATE),
    ),
    VehicleCommand.CLOSE_LIFTGATE: (
        _LIFTGATE,
        "body.closures.close",
        _closure(body_pb2.LIFTGATE),
    ),
    VehicleCommand.OPEN_CHARGE_PORT_DOOR: (
        _BODY,
        "body.closures.open",
        _closure(body_pb2.CHARGE_PORT),
    ),
    VehicleCommand.CLOSE_CHARGE_PORT_DOOR: (
        _BODY,
        "body.closures.close",
        _closure(body_pb2.CHARGE_PORT),
    ),
    VehicleCommand.PANIC_ON: (_SECURITY, "security.alarm.enable_panic", _empty),
    VehicleCommand.PANIC_OFF: (_SECURITY, "security.alarm.disable_panic", _empty),
    VehicleCommand.ENABLE_GEAR_GUARD_VIDEO: (
        _SECURITY,
        "security.video_monitoring.enable_video_monitoring",
        _empty,
    ),
    VehicleCommand.DISABLE_GEAR_GUARD_VIDEO: (
        _SECURITY,
        "security.video_monitoring.disable_video_monitoring",
        _empty,
    ),
    VehicleCommand.VEHICLE_CABIN_PRECONDITION_ENABLE: (
        _COMFORT,
        "comfort.cabin.enable_preconditioning",
        _empty,
    ),
    VehicleCommand.VEHICLE_CABIN_PRECONDITION_DISABLE: (
        _COMFORT,
        "comfort.cabin.disable_preconditioning",
        _empty,
    ),
    VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP: (
        _COMFORT,
        "comfort.cabin.set_preconditioning_temperature",
        _temperature,
    ),
    VehicleCommand.CABIN_HVAC_DEFROST_DEFOG: (
        _COMFORT,
        "comfort.cabin.set_defrost_defog",
        _defrost,
    ),
    VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT: _seat(comfort_pb2.SEAT_ROW_1_LEFT),
    VehicleCommand.CABIN_HVAC_RIGHT_SEAT_HEAT: _seat(comfort_pb2.SEAT_ROW_1_RIGHT),
    VehicleCommand.CABIN_HVAC_LEFT_SEAT_VENT: _seat(comfort_pb2.SEAT_ROW_1_LEFT, _VENT),
    VehicleCommand.CABIN_HVAC_RIGHT_SEAT_VENT: _seat(
        comfort_pb2.SEAT_ROW_1_RIGHT, _VENT
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
        _COMFORT,
        "comfort.cabin.set_cabin_surface",
        _surface(
            comfort_pb2.STEERING_WHEEL, comfort_pb2.CONDITIONING_HEAT, _WHEEL_LEVELS
        ),
    ),
    VehicleCommand.START_CHARGING: (_ENERGY, "charging.energy.start_charging", _empty),
    VehicleCommand.STOP_CHARGING: (_ENERGY, "charging.energy.stop_charging", _empty),
    VehicleCommand.CHARGING_LIMITS: (
        _ENERGY,
        "charging.energy.set_charge_limit",
        _charge_limit,
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

    `params` are those of `send_vehicle_command`.
    """
    if not (entry := _COMMANDS.get(command)):
        raise RivianBadRequestError(f"{command} has no Parallax equivalent")
    _, rvm, build = entry
    return rvm, build(params or {})
