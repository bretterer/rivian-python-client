"""Decoders for `body.*` RVM topics: closures, locks, trailer."""

from __future__ import annotations

from typing import Any, Final

from .core import _LOGGER, RVMDecoder, _enum, _present
from .proto import body_pb2

_CLOSURE_MAP: Final[dict[int, str]] = {
    body_pb2.DOOR_FRONT_LEFT: "doorFrontLeftClosed",
    body_pb2.DOOR_FRONT_RIGHT: "doorFrontRightClosed",
    body_pb2.DOOR_REAR_LEFT: "doorRearLeftClosed",
    body_pb2.DOOR_REAR_RIGHT: "doorRearRightClosed",
    body_pb2.FRUNK: "closureFrunkClosed",
    body_pb2.TAILGATE: "closureTailgateClosed",
    body_pb2.LIFTGATE: "closureLiftgateClosed",
    body_pb2.SIDE_BIN_LEFT: "closureSideBinLeftClosed",
    body_pb2.SIDE_BIN_RIGHT: "closureSideBinRightClosed",
    body_pb2.CHARGE_PORT: "chargePortState",
    body_pb2.TONNEAU: "closureTonneauClosed",
    body_pb2.WINDOW_FRONT_LEFT: "windowFrontLeftClosed",
    body_pb2.WINDOW_FRONT_RIGHT: "windowFrontRightClosed",
    body_pb2.WINDOW_REAR_LEFT: "windowRearLeftClosed",
    body_pb2.WINDOW_REAR_RIGHT: "windowRearRightClosed",
    body_pb2.WINDOW_REAR: "windowRearClosed",
}

_CLOSURE_STATE_MAP: Final[dict[int, str]] = {
    body_pb2.CLOSURE_STATE_OPEN: "open",
    body_pb2.CLOSURE_STATE_CLOSED: "closed",
    body_pb2.CLOSURE_STATE_AJAR: "ajar",
    body_pb2.CLOSURE_STATE_OPENING: "opening",
    body_pb2.CLOSURE_STATE_CLOSING: "closing",
}


def _enum_names(enum: Any, prefix: str) -> dict[int, str]:
    """Map an enum's numbers to its lowercased names, minus `prefix`."""
    return {
        value.number: value.name.removeprefix(prefix).lower()
        for value in enum.DESCRIPTOR.values
    }


_SIDE_BIN_NEXT_ACTIONS: Final = _enum_names(body_pb2.SideBinNextAction, "SIDE_BIN_")

# Closure id -> (next-action field, result key, value names).
_NEXT_ACTIONS: Final[dict[int, tuple[str, str, dict[int, str]]]] = {
    body_pb2.FRUNK: (
        "frunk_next_action",
        "closureFrunkNextAction",
        _enum_names(body_pb2.FrunkNextAction, "FRUNK_"),
    ),
    body_pb2.LIFTGATE: (
        "liftgate_next_action",
        "closureLiftgateNextAction",
        _enum_names(body_pb2.LiftgateNextAction, "LIFTGATE_"),
    ),
    body_pb2.SIDE_BIN_LEFT: (
        "side_bin_next_action",
        "closureSideBinLeftNextAction",
        _SIDE_BIN_NEXT_ACTIONS,
    ),
    body_pb2.SIDE_BIN_RIGHT: (
        "side_bin_next_action",
        "closureSideBinRightNextAction",
        _SIDE_BIN_NEXT_ACTIONS,
    ),
    body_pb2.TAILGATE: (
        "tailgate_next_action",
        "closureTailgateNextAction",
        _enum_names(body_pb2.TailgateNextAction, "TAILGATE_"),
    ),
    body_pb2.CHARGE_PORT: (
        "charge_port_door_next_action",
        "closureChargePortDoorNextAction",
        _enum_names(body_pb2.ChargePortDoorNextAction, "CHARGE_PORT_DOOR_"),
    ),
    body_pb2.GROUP_WINDOWS: (
        "windows_next_action",
        "windowsNextAction",
        _enum_names(body_pb2.WindowsNextAction, "WINDOWS_"),
    ),
}

_LOCK_MAP: Final[dict[int, str]] = {
    body_pb2.LOCK_DOOR_FRONT_LEFT: "doorFrontLeftLocked",
    body_pb2.LOCK_DOOR_FRONT_RIGHT: "doorFrontRightLocked",
    body_pb2.LOCK_DOOR_REAR_LEFT: "doorRearLeftLocked",
    body_pb2.LOCK_DOOR_REAR_RIGHT: "doorRearRightLocked",
    body_pb2.LOCK_FRUNK: "closureFrunkLocked",
    body_pb2.LOCK_TAILGATE: "closureTailgateLocked",
    body_pb2.LOCK_LIFTGATE: "closureLiftgateLocked",
    body_pb2.LOCK_SIDE_BIN_LEFT: "closureSideBinLeftLocked",
    body_pb2.LOCK_SIDE_BIN_RIGHT: "closureSideBinRightLocked",
    body_pb2.LOCK_CHARGE_PORT: "closureChargePortLocked",
    body_pb2.LOCK_TRUNK_SECURITY: "closureTrunkSecurityLocked",
    body_pb2.LOCK_CENTER_CONSOLE: "closureCenterConsoleLocked",
    body_pb2.LOCK_GLOVE_BOX: "closureGloveBoxLocked",
    body_pb2.LOCK_GEAR_GUARD: "gearGuardLocked",
    body_pb2.LOCK_TONNEAU: "closureTonneauLocked",
}

_LOCK_STATE_MAP: Final[dict[int, str]] = {
    body_pb2.LOCK_STATE_LOCKED: "locked",
    body_pb2.LOCK_STATE_UNLOCKED: "unlocked",
    body_pb2.LOCK_STATE_PARTIALLY_UNLOCKED: "partially_unlocked",
}

_TRAILER_PRESENCE_MAP: Final[dict[int, str]] = {
    body_pb2.TRAILER_NOT_PRESENT: "trailer_not_present",
    body_pb2.TRAILER_PRESENT: "trailer_present",
    body_pb2.TRAILER_PRESENT_WITH_BRAKES: "trailer_present_with_brakes",
    body_pb2.TRAILER_INVALID: "trailer_invalid",
}


@RVMDecoder.register("body.closures.states", body_pb2.ClosuresState)
def decode_closures(m: body_pb2.ClosuresState) -> dict[str, Any]:
    """body.closures.states — state of every door, window and closure.

    Fields:
        doorFrontLeftClosed, closureFrunkClosed, etc.: str
            ("open" | "closed" | "ajar" | "opening" | "closing")
        closureFrunkNextAction, closureLiftgateNextAction,
        closureTailgateNextAction, closureSideBinLeftNextAction,
        closureSideBinRightNextAction, closureChargePortDoorNextAction,
        windowsNextAction: str — e.g. "open_allowed" (shut),
            "close_allowed" (open); for the charge port,
            "close_not_available" means plugged in

    `chargePortState` can lag the door (e.g. "opening" until plugged in),
    so prefer its next action. After an app command, next actions briefly
    drop to "sna" / "open_not_available".
    """
    result: dict[str, Any] = {}
    for s in m.closure:
        cid = s.id
        state_val = _present(s, "state")
        if cid in _CLOSURE_MAP:
            result[_CLOSURE_MAP[cid]] = _enum(
                _CLOSURE_STATE_MAP, state_val, what="closure state"
            )
        elif cid != body_pb2.GROUP_WINDOWS:
            _LOGGER.debug("Unknown closure id %s (state %s)", cid, state_val)
        if cid in _NEXT_ACTIONS:
            field, key, names = _NEXT_ACTIONS[cid]
            if (next_action := _present(s, field)) is not None:
                result[key] = _enum(names, next_action, what=f"{key} value")
    return result


@RVMDecoder.register("body.locks.states", body_pb2.LocksState)
def decode_locks(m: body_pb2.LocksState) -> dict[str, Any]:
    """body.locks.states — lock state of every lock.

    Fields:
        doorFrontLeftLocked, closureFrunkLocked, gearGuardLocked (the Gear
            Guard cable), etc.: str ("locked" | "unlocked" |
            "partially_unlocked")
    """
    result: dict[str, Any] = {}
    for s in m.lock:
        lid = s.id
        state_val = _present(s, "state")
        if state_val is None:
            continue
        if lid in _LOCK_MAP:
            result[_LOCK_MAP[lid]] = _enum(
                _LOCK_STATE_MAP, state_val, what="lock state"
            )
        else:
            _LOGGER.debug("Unknown lock id %s (state %s)", lid, state_val)
    return result


@RVMDecoder.register("body.trailer.state", body_pb2.TrailerState)
def decode_trailer_state(m: body_pb2.TrailerState) -> dict[str, Any]:
    """body.trailer.state — trailer presence, with or without brakes.

    Fields:
        trailerStatus: str
    """
    result: dict[str, Any] = {}
    presence = _enum(
        _TRAILER_PRESENCE_MAP, _present(m, "presence"), what="trailer presence"
    )
    if presence is not None:
        result["trailerStatus"] = presence
    return result


@RVMDecoder.register("body.wipers.fluid_level", body_pb2.WiperFluidLevel)
def decode_wiper_fluid_level(m: body_pb2.WiperFluidLevel) -> dict[str, Any]:
    """body.wipers.fluid_level — washer fluid level.

    Fields:
        _wiperFluidLevel: int — raw
    """
    if (v := _present(m, "field_2")) is None:
        return {}
    return {"_wiperFluidLevel": v}
