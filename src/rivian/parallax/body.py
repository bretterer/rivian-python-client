"""Decoders for `body.*` RVM topics: closures, locks, trailer."""

from __future__ import annotations

from typing import Any, Final

from .core import _LOGGER, RVMDecoder, _enum, _present
from .proto import body_pb2

_CLOSURE_MAP: Final[dict[int, str]] = {
    1: "doorFrontLeftClosed",
    2: "doorFrontRightClosed",
    3: "doorRearLeftClosed",
    4: "doorRearRightClosed",
    5: "closureFrunkClosed",
    6: "closureTailgateClosed",
    7: "closureLiftgateClosed",
    8: "closureSideBinLeftClosed",
    9: "closureSideBinRightClosed",
    10: "chargePortState",
    11: "closureTonneauClosed",
    12: "windowFrontLeftClosed",
    13: "windowFrontRightClosed",
    14: "windowRearLeftClosed",
    15: "windowRearRightClosed",
}

_CLOSURE_STATE_MAP: Final[dict[int, str]] = {
    1: "open",
    2: "closed",
    4: "opening",
    5: "closing",
}


def _enum_names(enum: Any, prefix: str) -> dict[int, str]:
    """Map an enum's numbers to its lowercased names, minus `prefix`."""
    return {
        value.number: value.name.removeprefix(prefix).lower()
        for value in enum.DESCRIPTOR.values
    }


# Other side-bin values are unconfirmed, so they pass through as raw ints.
_SIDE_BIN_NEXT_ACTIONS: Final[dict[int, str]] = {
    body_pb2.SIDE_BIN_SNA: "sna",
    body_pb2.SIDE_BIN_OPEN_ALLOWED: "open_allowed",
}

# Closure id -> (next-action field, result key, value names).
_NEXT_ACTIONS: Final[dict[int, tuple[str, str, dict[int, str]]]] = {
    body_pb2.FRUNK: (
        "frunk_next_action",
        "closureFrunkNextAction",
        _enum_names(body_pb2.FrunkNextAction, "FRUNK_"),
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
}

_LOCK_MAP: Final[dict[int, str]] = {
    1: "doorFrontLeftLocked",
    2: "doorFrontRightLocked",
    3: "doorRearLeftLocked",
    4: "doorRearRightLocked",
    5: "closureFrunkLocked",
    6: "closureTailgateLocked",
    7: "closureLiftgateLocked",
    8: "closureSideBinLeftLocked",
    9: "closureSideBinRightLocked",
    15: "closureTonneauLocked",
}

_TRAILER_PRESENCE_MAP: Final[dict[int, str]] = {
    1: "trailer_not_present",
    2: "trailer_present",
    3: "trailer_present_with_brakes",
    4: "trailer_invalid",
}


@RVMDecoder.register("body.closures.states", body_pb2.ClosuresState)
def decode_closures(m: body_pb2.ClosuresState) -> dict[str, Any]:
    """body.closures.states — state of every door, window and closure.

    Fields:
        doorFrontLeftClosed, closureFrunkClosed, etc.: str
            ("open" | "closed" | "opening" | "closing")
        closureFrunkNextAction, closureTailgateNextAction,
        closureSideBinLeftNextAction, closureSideBinRightNextAction,
        closureChargePortDoorNextAction: str — e.g. "open_allowed" (shut),
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
        else:
            _LOGGER.debug("Unknown closure id %s (state %s)", cid, state_val)
        if cid in _NEXT_ACTIONS:
            field, key, names = _NEXT_ACTIONS[cid]
            if (next_action := _present(s, field)) is not None:
                result[key] = _enum(names, next_action, what=f"{key} value")
    return result


@RVMDecoder.register("body.locks.states", body_pb2.LocksState)
def decode_locks(m: body_pb2.LocksState) -> dict[str, Any]:
    """body.locks.states — lock state of every lockable closure.

    Fields:
        doorFrontLeftLocked, closureFrunkLocked, etc.: str ("locked" | "unlocked")
    """
    result: dict[str, Any] = {}
    for s in m.lock:
        lid = s.id
        state_val = _present(s, "state")
        if state_val is None:
            continue
        if lid in _LOCK_MAP:
            result[_LOCK_MAP[lid]] = "locked" if state_val == 1 else "unlocked"
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
        _wiperFluidLevel: int — raw (1 so far, presumably normal)
    """
    if (v := _present(m, "field_2")) is None:
        return {}
    return {"_wiperFluidLevel": v}
